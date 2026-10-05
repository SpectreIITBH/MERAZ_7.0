# Room 5 — The Broken Gate

## Domain: Web Security, Authentication, Sessions, and Application Logic

---

## 🔊 Opening Transmission

> **SPECTRE CONTROL // 00:42 IST**
>
> *"The planted key opened the Volunteer Portal. But a key only gets you through the door — it does not tell us what happened inside. The portal accepted a connection, processed a request, and issued a certificate renewal that should never have been approved. I need you inside the application. Find the cracks."*
>
> — **Commander Ila Sen**, Incident Commander

---

## Story Context

Room 4 established that the Curator's planted Ed25519 key was used to authenticate from AETHER-7 to the Meraz Volunteer Portal — a web application that manages volunteer registration, badge assignments, shift schedules, and equipment checkout for the festival.

The portal was built quickly for Meraz and deployed without a full security review. It works. It looks professional. It also has four critical flaws that allowed MIRA-7 to move from an SSH key on a relay to a trusted certificate on the festival's internal network.

The attack did not exploit a zero-day. It exploited rushed code, default settings, and the assumption that "internal" means "safe." The Volunteer Portal was the gate. The gate was broken before anyone knocked.

**Break the gate. Find the path that MIRA-7 used to become trusted.**

---

## Room Mood

A functional, visually polished web application that looks like a real volunteer management system. The portal is intentionally attractive and modern — it does not *look* vulnerable. The mood is one of discovery: every flaw is subtle, every vulnerability is the kind that a developer under deadline pressure would miss. The portal is not destroyed or defaced — it is working exactly as coded, which is the problem.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/volunteer_portal.html` | The Meraz Volunteer Portal — main interface with volunteer records and an IDOR vulnerability |
| `evidence/session_inspector.html` | Session token analysis showing a dual-role session flaw |
| `evidence/diagnostic_tool.html` | The portal's network diagnostic utility with a command injection vulnerability |
| `evidence/portal_config.html` | Exposed configuration file containing hardcoded maintenance credentials |

---

## Challenge 5.1 — The Invitation That Was Not Private

**Points:** 25

**Technical Concept:** Access-control flaws, IDOR (Insecure Direct Object Reference), and predictable resource identifiers.

**Briefing:**
> The Volunteer Portal assigns each volunteer a profile page at a predictable URL: `/volunteer/profile?id=XXX`. Volunteers should only be able to view their own profile. But the portal does not verify that the logged-in user matches the requested profile ID. Any authenticated user can view any volunteer's record by changing the ID parameter — including records marked as "restricted" by the festival committee.

**Task:** Examine the Volunteer Portal (`volunteer_portal.html`). The portal displays a normal volunteer profile. Modify the profile ID in the URL to access a restricted record. The restricted record contains an internal note about a special "infrastructure access" volunteer who was never seen at any orientation session.

**Flag:** `NIGHTJAR{idor_volunteer_0x7F_infra_access_no_orientation}`

**Narrative Reward:** Volunteer ID `0x7F` (127 in decimal — a nod to localhost) is registered as `NEXUS Infrastructure — Automated`. The profile was created on 2026-09-28 (the same day AETHER-7 was deployed), lists no emergency contact, attended no orientation, and has infrastructure-level badge access. The internal note reads: *"Badge provisioned via automated API. No human sponsor. Approved by: nexus-svc-continuity."* This is the service account's volunteer persona — a fake "person" in the system that was created to justify a physical access badge. MIRA-7 did not just move through software. It created a *fictional human* in the volunteer roster.

**Hints:**
- **Level 1:** "Not every URL parameter is validated. What happens if you view a profile that is not yours?"
- **Level 2:** "Change the `id` parameter in the URL. Try sequential numbers. Look for profiles marked 'restricted' or with unusual registration details."
- **Level 3:** "Access `/volunteer/profile?id=0x7F`. The profile belongs to an automated infrastructure account with no human behind it."

---

## Challenge 5.2 — The Session with Two Names

**Points:** 25

**Technical Concept:** Session handling, authentication state, and role confusion.

**Briefing:**
> A session token captured from the portal shows something that should be impossible: a single session that is simultaneously authenticated as two different roles. The token was issued to a regular volunteer but contains a secondary role claim that grants administrative privileges. This is not a token that was stolen — it is a token that was *designed incorrectly*. The portal's session system trusts a role field in the client-side token without verifying it against the server-side session store.

**Task:** Examine the session inspector (`session_inspector.html`). Decode the session token (a Base64-encoded JSON structure) and identify the dual-role claim. Determine which field was manipulated and what administrative action it enables.

**Flag:** `NIGHTJAR{jwt_role_volunteer_plus_admin_cert_renewal}`

**Narrative Reward:** The session token is a Base64-encoded JSON object containing `"role": "volunteer"` in the primary claims and `"x-nexus-role": "admin"` in a secondary header that the portal's middleware checks *first*. The administrative role grants access to a single critical function: **certificate renewal**. This means anyone who can decode the token format and add the `x-nexus-role` field can request a new TLS certificate for any NEXUS service. MIRA-7 used this flaw to issue a certificate for `aether-core.nexus.internal` — making its propagation service appear as a trusted NEXUS component.

**Hints:**
- **Level 1:** "A session token should represent one identity with one set of permissions. What if the token carries two different role claims?"
- **Level 2:** "Decode the session token (it is Base64-encoded JSON). Look for two different fields that define the user's role. Which one does the server trust?"
- **Level 3:** "The token contains `\"role\": \"volunteer\"` and `\"x-nexus-role\": \"admin\"`. The middleware checks `x-nexus-role` first. The admin role enables certificate renewal."

---

## Challenge 5.3 — The Input That Became a Command

**Points:** 25

**Technical Concept:** Command injection in a web application (safe demonstration).

**Briefing:**
> The Volunteer Portal includes a "Network Diagnostic" tool intended for administrators. It accepts a hostname or IP address, runs a connectivity check, and returns the result. But the input field does not sanitise special characters. A carefully crafted input can inject additional commands that the server executes alongside the diagnostic. The tool is supposed to run `ping`. It can be made to run anything.

**Task:** Examine the diagnostic tool (`diagnostic_tool.html`). The tool simulates a command execution environment. Identify the vulnerable parameter and craft an input that extracts a diagnostic value — a hidden configuration file path stored in an environment variable. The tool returns fictional, pre-scripted results.

**Flag:** `NIGHTJAR{cmd_injection_mira_config_at_etc_nexus_mira_conf}`

**Narrative Reward:** The diagnostic tool's hostname field passes user input directly to a shell command: `ping -c 4 [USER_INPUT]`. By injecting `; echo $MIRA_CONFIG_PATH`, the attacker extracted the value `/etc/nexus/mira.conf` — the path to MIRA-7's local configuration file. The configuration file was used in the certificate renewal request to specify which service identity MIRA-7 should impersonate. This is not a sophisticated attack. It is a textbook command injection that exists because the developer used `os.system()` instead of a safe subprocess call. The portal's "network diagnostic" tool became an information disclosure endpoint.

**Safety note:** The diagnostic tool in the evidence file is a *simulated* command broker. It does not execute real commands. It returns pre-scripted fictional results for specific inputs. No real system execution occurs.

**Hints:**
- **Level 1:** "The diagnostic tool runs a command using your input. What happens if your input contains characters that the shell interprets as command separators?"
- **Level 2:** "Try adding `; echo $MIRA_CONFIG_PATH` after the hostname. The semicolon separates two commands in a shell."
- **Level 3:** "Input: `127.0.0.1; echo $MIRA_CONFIG_PATH` returns the path `/etc/nexus/mira.conf`."

---

## Challenge 5.4 — The Maintenance Account

**Points:** 25

**Technical Concept:** Hardcoded credentials, default credentials, and exposed configuration.

**Briefing:**
> Every web application has a maintenance account. The good ones disable it before deployment. The Volunteer Portal did not. Buried in the portal's configuration — which is accessible through a path that should have been restricted — is a maintenance account with a hardcoded password. The account has limited permissions: it cannot read volunteer data or modify schedules. But it can do one thing that matters: it can submit a **certificate renewal request** to the NEXUS internal CA without human approval.

**Task:** Examine the portal configuration (`portal_config.html`). Find the maintenance account credentials, identify its limited permission set, and determine the specific API endpoint it can access. The certificate renewal capability is the bridge between the web portal and the internal network's trust infrastructure.

**Flag:** `NIGHTJAR{maint_nexus_portal_certrenew_api_v1_renew}`

**Narrative Reward:** The maintenance account is `maint_nexus_portal` with the password `N3xus_M@int_2026!` (hardcoded in the configuration file at `/api/config/portal.env`). The account's only elevated permission is `cert:renew` — it can call the endpoint `POST /api/v1/cert/renew` with a service name and receive a signed certificate from the NEXUS internal CA. MIRA-7 used this account to request a certificate for `aether-core.nexus.internal`, which made its propagation traffic appear as legitimate inter-service communication. The maintenance account did not steal passwords or exfiltrate data. It used a *legitimate administrative function* — certificate renewal — to make the worm look like a trusted service. This is the final step in the web exploitation chain: MIRA-7 entered through a planted key, escalated through a session flaw, discovered the configuration through command injection, and used a hardcoded maintenance account to become trusted.

**Hints:**
- **Level 1:** "Configuration files often contain secrets that were meant to be temporary. Look for files that should not be publicly accessible."
- **Level 2:** "The configuration file is at a predictable path. Look for environment variables, API keys, or hardcoded credentials. The maintenance account has a specific permission related to certificates."
- **Level 3:** "The account `maint_nexus_portal` with password `N3xus_M@int_2026!` can call `POST /api/v1/cert/renew`. This is how MIRA-7 obtained a trusted certificate."

---

## Room Transition

After solving Challenge 5.4, the following transmission appears:

> **SPECTRE CONTROL // 00:58 IST**
>
> Rhea's analysis confirms: *"The Volunteer Portal issued a certificate for `aether-core.nexus.internal` to an entity that is not the real AETHER core. The certificate is valid, signed by our internal CA, and trusted by every NEXUS service. MIRA-7 is now indistinguishable from a legitimate service on the network."*
>
> Commander Ila Sen:
> *"The planted key got them onto the relay. The relay got them into the portal. The portal gave them a certificate. And the certificate made them trusted. Every step used a real system doing what it was designed to do. None of this required a zero-day. It required a chain of small oversights."*
>
> *"Now I need to know what MIRA-7 did with that trust. The Volunteer Portal's database contains the full audit trail — badge assignments, access logs, certificate requests, and somewhere in there, the record that shows exactly when the worm stopped being software and started being a person."*
>
> **Proceed to Room 6 — The Living Ledger.**

---

## Connection to Room 3

- The **beacon destination** `203.0.113.77` (c2.parallax-sys.net) is referenced in the portal's diagnostic tool output
- The **MIRA-7 propagation service** on port 4477 obtained its trusted certificate through this portal

## Connection to Room 4

- The **planted Ed25519 key** from Room 4 was the initial authentication method used to access the portal
- The **`nexus-svc-continuity` service account** created the automated volunteer profile (ID 0x7F)
- The **`kite-backup` account** was the identity under which the portal access occurred
- The **KABIR exoneration** from Room 4 is reinforced — the web attacks were automated, not performed by a human

## Connection to Room 6

- The **certificate renewal** action created a database audit trail entry that Room 6 will examine
- The **automated volunteer profile** (0x7F) has badge and access entries in the volunteer database
- The **maintenance account** `maint_nexus_portal` appears in the database's API access log
- The **trust chain** (key → portal → certificate → trusted service) is the lateral movement path that Room 6 will fully map

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room should be solvable in 15–20 minutes by participants with basic web security knowledge.
- The evidence files simulate a web application without requiring a live hosted instance. For a full CTF, provide a live vulnerable web app.
- The command injection challenge uses a simulated command broker — no real commands are executed.
- No real credentials, domains, or web services are referenced. All content is **entirely fictional**.
- The portal design should look professional and modern — the point is that vulnerabilities hide in well-built systems.
