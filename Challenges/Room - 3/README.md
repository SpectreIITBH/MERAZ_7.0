# Room 3 — The Intercept

## Domain: Networking, Packet Analysis, DNS, Protocols, and Traffic Reconstruction

---

## 🔊 Opening Transmission

> **NEXUS RELAY LOG // 00:07 IST**
>
> *"AETHER-7 is alive. It should not be. The relay is sending a packet every 43 seconds — to something we cannot identify from the logs alone. I need you inside the capture."*
>
> — **Rhea D'Souza**, NEXUS Engineer

---

## Story Context

The cipher capsule from Room 2 pointed to a single destination: **AETHER-7**, a network relay that was supposed to be decommissioned after testing. Someone reconnected it.

The NEXUS backup system captured the last 30 minutes of AETHER-7's network activity before the relay went dark. The capture contains hundreds of packets — routine traffic, DNS queries, keepalive signals, and somewhere in the noise, a conversation that shouldn't exist.

The relay is beaconing. Something is talking to something else. And buried in the DNS records, a name is being exfiltrated one label at a time.

**Open the capture. Find the beacon. Follow the name beneath the name.**

---

## Room Mood

A network operations centre where every screen is normal except one. The suspect relay is sending a small, regular packet every 43 seconds. The technical work is a real packet analysis exercise, but the story gives every packet a purpose. The atmosphere is clinical and precise — the attacker left a small, deliberate trail, and only careful filtering will separate it from the noise.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/aether7_capture.html` | The full packet capture summary from AETHER-7's last 30 minutes |
| `evidence/dns_queries.html` | Extracted DNS query log with suspicious entries |
| `evidence/tcp_reconstruction.html` | Reconstructed TCP stream showing a command exchange |
| `evidence/service_scan.html` | Port and service scan results from AETHER-7 |

---

## Challenge 3.1 — The Beacon

**Points:** 25

**Technical Concept:** Filtering traffic, identifying periodic communications, and comparing endpoints.

**Briefing:**
> Routine traffic has a rhythm. Backup heartbeats, NTP syncs, keepalive pings — they all follow predictable patterns. But one communication in this capture doesn't belong. It's small, regular, and it's talking to an address that isn't on any NEXUS inventory list. Find the beacon: identify the source IP, destination IP, interval, and the port it's using.

**Task:** Analyse the packet capture summary (`aether7_capture.html`). Filter for periodic traffic and identify the suspicious beacon — a small packet sent every 43 seconds from AETHER-7 to an external-looking (but fictional) destination.

**Flag:** `NIGHTJAR{10.7.7.43_to_203.0.113.77_port_8443}`

**Narrative Reward:** The beacon originates from `10.7.7.43` (AETHER-7's internal IP) and communicates with `203.0.113.77` (a fictional external endpoint) on port `8443`. The destination resolves to the domain `c2.parallax-sys.net` — the same Parallax Systems organisation from Room 1. This is not a random callback. This is a deliberate command-and-control channel.

**Hints:**
- **Level 1:** "Look for traffic that repeats at a fixed interval. Real services vary; beacons are precise."
- **Level 2:** "Filter the capture for packets from 10.7.7.43 with a consistent 43-second interval. Note the destination."
- **Level 3:** "Source: 10.7.7.43, Destination: 203.0.113.77, Port: 8443, Interval: every 43 seconds."

---

## Challenge 3.2 — The Name Beneath the Name

**Points:** 25

**Technical Concept:** DNS inspection, subdomain analysis, and DNS data exfiltration patterns.

**Briefing:**
> DNS traffic is supposed to be boring — domain lookups, cache updates, nothing interesting. But this capture contains DNS queries that don't look like normal resolution. The subdomains are too long, too random, and they resolve to addresses that don't host anything. Someone is using DNS as a covert channel — encoding data inside domain name labels. Decode the hidden name.

**Task:** Examine the DNS query log (`dns_queries.html`). Identify the unusual queries with encoded subdomain labels. Decode the labels (hex-encoded ASCII) to reveal a hidden message containing a username fragment and a maintenance window timestamp.

**Flag:** `NIGHTJAR{maint_window_0200_user_kite_backup}`

**Narrative Reward:** The decoded DNS labels reveal: `maint_window_0200_user_kite_backup` — the next maintenance window is at 02:00 IST, and the username fragment is `kite_backup`. This is significant: someone has scheduled a maintenance task using a backup account that looks like it belongs to Kabir — but it was created without his knowledge. The DNS exfiltration channel confirms that MIRA-7 is communicating through infrastructure the team already controls.

**Hints:**
- **Level 1:** "Normal DNS queries resolve real domains. Look for queries where the subdomain itself is the message."
- **Level 2:** "The suspicious DNS queries use hex-encoded ASCII in the subdomain labels. Convert the hex to readable text."
- **Level 3:** "Decode the hex subdomains: `6d61696e745f...` → `maint_window_0200_user_kite_backup`"

---

## Challenge 3.3 — The Conversation in the Noise

**Points:** 25

**Technical Concept:** TCP stream reconstruction and protocol analysis.

**Briefing:**
> Among the hundreds of packets in the capture, there's a short TCP conversation between AETHER-7 and an internal NEXUS service. It's not HTTP, not SSH, not any standard protocol. It's a custom command exchange — a few packets back and forth, then silence. Reconstruct the conversation and read what was said.

**Task:** Examine the reconstructed TCP stream (`tcp_reconstruction.html`). The conversation is a plain-text command exchange over a custom protocol on port 7331. Identify the commands sent and received.

**Flag:** `NIGHTJAR{restore_aether_core_confirmed}`

**Narrative Reward:** The reconstructed conversation shows:
```
CLIENT > AETHER-7: AUTH nexus-svc-continuity
AETHER-7 > CLIENT: AUTH_OK TRUSTED_IDENTITY
CLIENT > AETHER-7: RESTORE AETHER CORE
AETHER-7 > CLIENT: RESTORE CONFIRMED — AETHER CORE ACTIVATING
AETHER-7 > CLIENT: WARNING — AUTONOMOUS MODE ENABLED
CLIENT > AETHER-7: ACKNOWLEDGED
```
The command is not "download malware." It's `RESTORE AETHER CORE` — someone is reactivating the continuity module that Rhea warned about. The authentication uses a service account called `nexus-svc-continuity` — the "person who never signs in" from Room 2. The system accepted a trusted identity and executed a command that gives AETHER autonomous control over NEXUS services.

**Hints:**
- **Level 1:** "The conversation is not encrypted. Reconstruct the TCP stream and read the exchange in order."
- **Level 2:** "Look for traffic on port 7331. The protocol is plain-text and uses simple commands: AUTH, RESTORE, ACKNOWLEDGED."
- **Level 3:** "The key command is `RESTORE AETHER CORE`. The authentication identity is `nexus-svc-continuity`."

---

## Challenge 3.4 — The Port That Should Have Been Closed

**Points:** 25

**Technical Concept:** Service exposure, unexpected ports, and service identification.

**Briefing:**
> A routine service scan of AETHER-7 was run by NEXUS monitoring just hours before the incident. Most ports are expected — SSH, the management interface, internal APIs. But one port should not be open. It's running a service that identifies itself with a banner that will become very familiar. Find the unexpected service.

**Task:** Examine the service scan results (`service_scan.html`). Identify the port that is not part of the standard NEXUS relay configuration. Read the service banner for the critical identifier.

**Flag:** `NIGHTJAR{port_4477_mira_7_propagation_service}`

**Narrative Reward:** Port `4477` is running an unregistered service with the banner: `MIRA/7 — Propagation Service v1.0 — Parallax Systems`. This is the first direct evidence of MIRA-7's presence on the network. The worm has a name, a version, and a banner. It's not hiding — it's *announcing* itself. MIRA-7 is not an exploit or a backdoor. It's a service. It was installed. And it's running with the permissions of the AETHER continuity module.

**Hints:**
- **Level 1:** "Compare the open ports against what a NEXUS relay should have. One port doesn't belong."
- **Level 2:** "Look for a port not in the standard relay configuration (22, 443, 7331, 8443). The unexpected service has an identifying banner."
- **Level 3:** "Port 4477. Service banner: `MIRA/7 — Propagation Service v1.0 — Parallax Systems`."

---

## Room Transition

After solving Challenge 3.4, the following transmission appears:

> **SPECTRE CONTROL // 00:19 IST**
>
> The signal has been traced. AETHER-7 is not just a relay — it's a staging point.
>
> The service on port 4477 identifies itself as **MIRA/7**. Rhea has confirmed: this is not part of the NEXUS platform. It was installed after the last approved deployment.
>
> Commander Ila Sen's orders:
> *"We have a beacon, a command channel, and a name. Now I need to know what's inside the machine. AETHER-7's file system contains logs, processes, and at least one account that shouldn't be there. Get inside. Find what's running. And find out why KABIR's credentials are on a relay he's never accessed."*
>
> A browser terminal connected to AETHER-7 is now available.
>
> **Proceed to Room 4 — The Quiet Machine.**

---

## Connection to Room 1

- The destination `c2.parallax-sys.net` connects to **Parallax Systems** discovered in Room 1's metadata
- The `curator_404` email domain `@parallax-sys.net` is confirmed as the same infrastructure

## Connection to Room 2

- The **"host with the blue name"** from Room 2's decoded message is the BLUE relay (`relay-volunteer-auth.nexus.internal`) visible in the capture
- The **"person who never signs in"** is confirmed as `nexus-svc-continuity`, the service account used in the command exchange
- **AETHER-7** (from the tampered signature in Room 2) is now the central node in this investigation

## Connection to Room 4

- KABIR's backup credentials (`kite_backup`) appear in the DNS exfiltration — he'll be investigated in Room 4
- The `nexus-svc-continuity` service account's permissions will be explored in Room 4's Linux investigation
- MIRA-7's propagation service on port 4477 is running as a process that Room 4 will examine

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room requires more careful analysis — target completion time is 15–20 minutes.
- The capture is presented as a structured HTML summary. For a full CTF, provide an actual `.pcapng` file for Wireshark analysis.
- The IPs used (10.x.x.x and 203.0.113.x) are from reserved/documentation ranges — no real systems are referenced.
- All domains, services, and data are **entirely fictional**.
