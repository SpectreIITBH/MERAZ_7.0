# Room 4 — The Quiet Machine

## Domain: Linux, Processes, Permissions, Persistence, Logs, and System Security

---

## 🔊 Opening Transmission

> **SPECTRE CONTROL // 00:19 IST**
>
> *"AETHER-7 is not just a relay — it is a staging point. A browser terminal is now connected to the machine. Find what is running, find who logged in, and find out why KABIR's credentials are on a relay he has never accessed."*
>
> — **Commander Ila Sen**, Incident Commander

---

## Story Context

The network capture from Room 3 confirmed that AETHER-7 is hosting MIRA-7's propagation service and beaconing to a Parallax Systems command-and-control domain. Commander Ila Sen has ordered a forensic examination of the relay itself.

A browser terminal connected to a snapshot of AETHER-7's filesystem is now available. The machine is a small Debian-based Linux relay that was supposed to be air-gapped after testing. Someone reconnected it, installed a service, created an account, and planted a key — all without generating a standard deployment ticket.

KABIR's name is everywhere on this machine. His credentials, his SSH key comment, his username in the crontab. But the timestamps tell a different story: the account was configured after KABIR last changed his password, the key was generated on hardware he has never owned, and the crontab entry was written by a script, not a human.

**Get inside the machine. Separate the evidence from the framing.**

---

## Room Mood

A clean, quiet Linux terminal. The machine is not destroyed or obviously compromised — it looks like a well-maintained server with a few extra entries that do not belong. The mood is one of careful forensic work: every file, process, timestamp, and permission tells a story, but the obvious story is a lie. The attacker did not ransack the machine. They set it up to look like KABIR did everything.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/process_list.html` | Output of `ps aux` showing all running processes on AETHER-7 |
| `evidence/auth_log.html` | Authentication log (`/var/log/auth.log`) showing login events and session activity |
| `evidence/filesystem_snapshot.html` | Key filesystem areas: crontab, systemd units, unusual files and their permissions |
| `evidence/ssh_keys.html` | Contents of `/home/kite-backup/.ssh/authorized_keys` and key metadata |

---

## Challenge 4.1 — The Process with a Clean Name

**Points:** 25

**Technical Concept:** Process inspection and persistence detection.

**Briefing:**
> The system is running 47 processes. Most of them are standard Linux daemons — sshd, cron, nginx, systemd services. But one process is trying very hard to look like it belongs. Its name is clean, its PID is unremarkable, and its parent is init. But its binary path does not match any installed package, and its resource usage is suspiciously regular. Find the imposter.

**Task:** Examine the process list (`process_list.html`). Identify the process that is not a standard system daemon. Note its name, PID, binary path, the user running it, and its CPU/memory pattern. The process name mimics a legitimate service but runs from a non-standard directory.

**Flag:** `NIGHTJAR{nexus_health_monitor_pid_2847_opt_mira}`

**Narrative Reward:** The process is called `nexus-health-monitor` (PID 2847) and runs from `/opt/.mira/nexus-health-monitor`. It looks like a legitimate NEXUS monitoring daemon, but no such package exists in the APT database. The binary was placed in a hidden directory under `/opt/` and registered as a systemd service called `nexus-healthd.service`. It runs as the user `nexus-svc-continuity` — the same service account from Room 3's TCP exchange. This is MIRA-7's persistence mechanism: a process that looks like maintenance but is the worm's local controller.

**Hints:**
- **Level 1:** "Not every process with a clean name was installed by the system. Compare the binary paths against standard Linux directories."
- **Level 2:** "Look for processes running from `/opt/` subdirectories. Legitimate packages install to `/usr/bin/` or `/usr/sbin/`. Hidden directories start with a dot."
- **Level 3:** "The process `nexus-health-monitor` (PID 2847) runs from `/opt/.mira/`. It runs as `nexus-svc-continuity`. This is not a real health monitor."

---

## Challenge 4.2 — The User Who Arrived Without a Login

**Points:** 25

**Technical Concept:** Authentication logs, account activity, and session analysis.

**Briefing:**
> The auth log contains a week of login events. SSH sessions, sudo commands, cron invocations — the usual noise of a managed Linux host. But one session is wrong. An account authenticated successfully, ran privileged commands, and exited cleanly — but there is no corresponding interactive login, no SSH key exchange, and no password prompt. The account "arrived" on the machine without any of the standard authentication markers.

**Task:** Examine the authentication log (`auth_log.html`). Identify the account that performed privileged actions without a standard SSH or console login. Determine the authentication method used and the timestamp of the suspicious session.

**Flag:** `NIGHTJAR{kite_backup_session_via_auth_token_0137}`

**Narrative Reward:** The account `kite-backup` opened a session at 01:37 IST — but the auth log shows no SSH key acceptance, no password check, and no PAM interactive login. Instead, the session was created via a PAM module called `pam_nexus_token.so` — a custom authentication module that accepts NEXUS service tokens instead of passwords. This module was installed as part of the AETHER continuity system and was never removed. The token used to authenticate was issued to `nexus-svc-continuity`, which means the service account from Room 3 created a session *as KABIR's backup account* using a trust delegation that no human approved. KABIR never logged in. The machine used his name.

**Hints:**
- **Level 1:** "A login without a password prompt or key exchange is not normal SSH. Look for alternative PAM modules."
- **Level 2:** "Search the auth log for sessions that show 'session opened' without a preceding 'Accepted publickey' or 'Accepted password'. Look for a custom PAM module name."
- **Level 3:** "The account `kite-backup` authenticated via `pam_nexus_token.so` at 01:37 IST. No human was involved — the token was issued by `nexus-svc-continuity`."

---

## Challenge 4.3 — The Permission That Lied

**Points:** 25

**Technical Concept:** Linux permissions, ownership, SUID concepts, and privilege boundaries.

**Briefing:**
> The `kite-backup` account is a low-privilege user — it should not be able to install services, modify system configuration, or write to protected directories. But the filesystem tells a different story. A specific file has permissions that allow `kite-backup` to execute it with elevated privileges. The file is not a standard SUID binary. It is a custom script with a very specific purpose: it restarts the AETHER continuity service with root permissions, no questions asked.

**Task:** Examine the filesystem snapshot (`filesystem_snapshot.html`). Identify the file with the unusual permissions, its ownership, its SUID/capability configuration, and what it does when executed. Explain why a low-privilege account can influence a root-level service restart.

**Flag:** `NIGHTJAR{suid_aether_restart_owned_by_root_writable_by_nexus}`

**Narrative Reward:** The file `/opt/.mira/aether-restart.sh` is owned by `root:nexus-svc` with permissions `-rwsr-x---` (SUID set, group-executable by `nexus-svc` group). The `kite-backup` account is a member of the `nexus-svc` group. When any member of this group executes the script, it runs as root and restarts the `aether-core.service` — the continuity module that was supposed to be decommissioned. The script also writes a flag file to `/var/run/aether.active` which tells the health monitor to begin propagation. This is the privilege escalation path: a low-privilege account, given group membership by a token-based login, can trigger a root-level service restart through a SUID script that was never audited.

**Hints:**
- **Level 1:** "Privilege does not always come from sudo. Check for files with special permission bits — SUID allows execution as the file owner."
- **Level 2:** "Look in the filesystem snapshot for files with the 's' bit set in their permissions. Check the `/opt/.mira/` directory and note the group ownership."
- **Level 3:** "The file `/opt/.mira/aether-restart.sh` has SUID set and is owned by root. The `nexus-svc` group can execute it, and `kite-backup` is in that group."

---

## Challenge 4.4 — The Key in the Drawer

**Points:** 25

**Technical Concept:** SSH key handling, key fingerprints, and authorised-key inspection.

**Briefing:**
> KABIR's backup account has an SSH authorized_keys file. One key in the file is expected — it was generated during the original NEXUS deployment. But a second key was added later. Its comment says `kite-backup-2019`, suggesting it was created in 2019. But the key's fingerprint, algorithm, and the timestamp of its addition tell a different story entirely. This key was generated *after* KABIR's current laptop was issued, using a tool he has never installed.

**Task:** Examine the SSH keys file (`ssh_keys.html`). Identify the unauthorised key by comparing the two entries: their algorithms, fingerprints, comments, and the timestamps of when they were added to the file. Determine when the second key was actually created and what tool generated it.

**Flag:** `NIGHTJAR{ed25519_kite_backup_2019_added_oct_2026_aetherforge}`

**Narrative Reward:** The first key is a standard RSA-4096 key with the comment `kabir@nexus-deploy-2024` — this is the legitimate deployment key. The second key is an Ed25519 key with the comment `kite-backup-2019`. But Ed25519 was not commonly used in 2019, and the file's modification timestamp shows it was added on 2026-10-01 — three days before the incident. The key's fingerprint does not match any key on KABIR's laptop or any NEXUS-issued device. The key was generated by `AetherForge v2.1` (the same tool from Room 1's banner EXIF data), confirming that the Curator's infrastructure planted this key to create a persistent backdoor using KABIR's name. **KABIR is not the attacker. He is the cover story.**

**Mid-story reveal:** The team now has definitive evidence that KABIR was framed. His name was used by a service account operating through a trust relationship he never authorised. The real entry point is the SSH key planted by the Curator's toolchain — and that key was accepted by the **Meraz Volunteer Portal**, which is the next target.

**Hints:**
- **Level 1:** "A key's comment can say anything. Look at the key algorithm and the file modification timestamp to verify the comment's claim."
- **Level 2:** "Compare the two keys. One is RSA, one is Ed25519. Check when the Ed25519 key was added to the authorized_keys file. Does the date match the comment?"
- **Level 3:** "The Ed25519 key with comment `kite-backup-2019` was added on 2026-10-01. It was generated by `AetherForge v2.1`, not by KABIR."

---

## Room Transition

After solving Challenge 4.4, the following transmission appears:

> **SPECTRE CONTROL // 00:38 IST**
>
> Rhea confirms: *"The Ed25519 key in KABIR's authorized_keys file is not his. It was generated by the same toolchain that built the festival banner. The key has been used exactly once — to authenticate to the Meraz Volunteer Portal's administrative API."*
>
> Commander Ila Sen:
> *"KABIR is clear. He is embarrassed, not guilty. But the key that was planted in his name opened a door somewhere. The Volunteer Portal accepted a connection from AETHER-7 using this key three days ago. I need to know what the portal let in — and why it did not ask any questions."*
>
> The Meraz Volunteer Portal is now available for investigation.
>
> **Proceed to Room 5 — The Broken Gate.**

---

## Connection to Room 2

- The **"person who never signs in"** (`nexus-svc-continuity`) is confirmed as the service account running the hidden process and creating token-based sessions
- The **AETHER-7** relay from Room 2's tampered signature is the machine under investigation

## Connection to Room 3

- The **beacon** to `203.0.113.77` (c2.parallax-sys.net) is controlled by the `nexus-health-monitor` process discovered in Challenge 4.1
- The **custom protocol on port 7331** was used by the same service account that created the `kite-backup` session
- **MIRA-7's propagation service** on port 4477 is managed by the same systemd unit as the health monitor
- The **DNS exfiltration** username `kite_backup` matches the planted account on this machine

## Connection to Room 5

- The **Ed25519 key** planted in `kite-backup`'s authorized_keys was used to authenticate to the Volunteer Portal
- The **`pam_nexus_token.so`** module demonstrates the trust delegation pattern that the portal also uses
- The **KABIR exoneration** changes how teams approach Room 5 — they are no longer looking for an insider but for a system vulnerability

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room should be solvable in 15–20 minutes by participants with basic Linux knowledge.
- The evidence is presented as HTML snapshots of terminal output. For a full CTF, provide a live container terminal.
- No real system access is required — all evidence is inspectable in a browser.
- All users, keys, paths, processes, and services are **entirely fictional**.
