# Room 7 — The False Victim

## Domain: Social Engineering, Identity, Authentication, and Human Factors

---

## 🔊 Opening Transmission

> **SPECTRE CONTROL // 01:28 IST**
>
> *"We have the path. Planted key. Compromised portal. Forged certificate. Stolen trust map. Implicit trust chain to the release controller. Every step was automated, efficient, and invisible. But the entire chain has a single origin: KABIR clicked a file. And I do not believe that was an accident."*
>
> *"Someone studied the festival's schedule, identified the one person with enough access and enough pressure to act without thinking, and sent a message that looked like salvation. This was not a mass phishing campaign. This was a precision strike against one human being. Find the message. Reconstruct the manipulation. And tell me whether KABIR was a careless insider or a carefully chosen target."*
>
> — **Commander Ila Sen**, Incident Commander

---

## Story Context

Rooms 4–6 traced the technical attack chain from AETHER-7 to the NEXUS Release Controller. Every step was automated, executed by the `nexus-svc-continuity` service account, and designed to look like legitimate system activity. But the entire chain required a trigger: a human action that gave the Curator's infrastructure its initial foothold.

That human action was KABIR "Kite" Mehra downloading and running a file called `Ethereal_Sync_Helper.exe` — the same file that Room 8 will examine as a malware sample. But before the malware can be analysed, the team needs to understand *how* KABIR was convinced to run it.

The answer is not stupidity. It is social engineering — a carefully constructed message that arrived at exactly the right moment, from what appeared to be exactly the right source, with exactly the right urgency. The Curator did not send a mass email to the festival. The Curator studied KABIR's work patterns, identified a moment of maximum stress, and crafted a message that looked like the solution to a real problem.

This room examines the human side of the breach: the phishing message, the authentication timeline, the MFA bypass, and the identity confusion that made the attack invisible until it was too late.

**The question is not "Did KABIR make a mistake?" The question is "Was the mistake designed for him?"**

---

## Room Mood

A timeline of messages, login events, and incident reports that reads like a short story about a person trying to do their job under pressure. The mood is empathetic, not accusatory: the evidence shows that KABIR was targeted because he was competent, not because he was careless. The phishing message is so well-crafted that participants should feel a moment of "I might have clicked that too." The room's emotional core is the realisation that social engineering exploits trust, not ignorance.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/phishing_timeline.html` | The complete message thread showing the phishing campaign against KABIR, with contextual timing analysis |
| `evidence/login_analysis.html` | Authentication log showing KABIR's real sessions alongside the impossible login from a different continent |
| `evidence/mfa_bypass.html` | MFA push notification timeline showing the fatigue attack that completed the initial compromise |
| `evidence/identity_graph.html` | Identity correlation matrix distinguishing humans, service accounts, and replayed personas |

---

## Challenge 7.1 — The Message That Arrived at the Right Time

**Points:** 25

**Technical Concept:** Phishing indicators and contextual social engineering.

**Briefing:**
> On September 27th, KABIR received a message through the festival's internal communication system. The message appeared to come from `nexus-support@meraz-festival.internal` — the official NEXUS technical support address. It referenced a real problem: the festival's ceremony automation scripts had been failing intermittently for two days. It offered a solution: a synchronisation tool called "Ethereal Sync" that would fix the timing issues. The message included a download link, installation instructions, and a deadline: "Please install before the tech review on September 28th."
>
> Every element of the message was calculated. The sender address was spoofed but used the correct internal domain format. The problem it described was real — KABIR had filed a ticket about it three days earlier. The tool name matched a legitimate NEXUS utility naming convention. And the deadline was real — there was a tech review on September 28th. The only thing that was fake was the solution.

**Task:** Examine the phishing timeline (`phishing_timeline.html`). Identify the specific signals that made the message convincing: the spoofed sender, the reference to a real problem, the naming convention match, the deadline alignment, and the emotional pressure. Then identify the indicators that *should* have revealed it as a phishing attempt — the ones that a person under deadline pressure would miss.

**Flag:** `NIGHTJAR{phish_kabir_sep27_nexus_support_spoofed_real_ticket_ref}`

**Narrative Reward:** The phishing message was not a generic "click this link" email. It was a **spear-phishing** attack that required:
- Access to the festival's internal ticket system (to reference KABIR's real ticket #NX-2847)
- Knowledge of the NEXUS naming conventions (to name the tool "Ethereal Sync Helper")
- Access to the festival calendar (to reference the real September 28th tech review)
- Understanding of KABIR's role and stress level (to frame the message as urgent help, not a request)

The indicators that should have revealed the deception:
- The sender domain used a hyphen (`meraz-festival.internal`) instead of an underscore (`meraz_festival.internal`)
- The download link pointed to `cdn-nexus.parallax-sys.net` — a Parallax Systems domain, not a NEXUS domain
- The PGP signature on the message was self-signed, not from the NEXUS team's keyring
- The "tool" had no entry in the NEXUS package registry

But KABIR was three days behind on ceremony automation. His manager had asked for a status update. The tech review was the next morning. And the message looked like the fix he needed. He clicked it because he was trying to save the festival.

**Hints:**
- **Level 1:** "A convincing phishing message does not just look official. It arrives at the moment when the target most needs what it offers. What was KABIR's situation when the message arrived?"
- **Level 2:** "Compare the sender address format against the real NEXUS support address. Check the download domain. Look for a reference to a real ticket number that the attacker should not have known."
- **Level 3:** "The sender used `meraz-festival.internal` (hyphen) instead of `meraz_festival.internal` (underscore). The download domain is `parallax-sys.net`. The message references ticket #NX-2847, which is KABIR's real ticket."

---

## Challenge 7.2 — The Login That Did Not Belong

**Points:** 25

**Technical Concept:** Impossible travel, session anomalies, and authentication telemetry.

**Briefing:**
> The authentication log for KABIR's account shows 47 login events over the past two weeks. Most are from the IIT Bhilai campus network (`10.0.0.0/8` internal range) or from KABIR's home IP (via the festival VPN). The sessions follow a regular pattern: morning logins, evening work sessions, occasional late-night pushes before deadlines.
>
> But one session does not fit. At `2026-10-01 01:35:42 IST`, a login was recorded from an IP address geolocated to Amsterdam, Netherlands. KABIR was on campus at IIT Bhilai at the time — verified by his badge scan at the Main Gate at `01:20 IST`. A person cannot be in Chhattisgarh, India and Amsterdam, Netherlands at the same time. The session lasted 4 minutes, accessed the NEXUS administrative API, and downloaded the ceremony automation script repository.

**Task:** Examine the login analysis (`login_analysis.html`). Find the login event that could not have come from KABIR. Identify the source IP, its geolocation, the timestamp, the session duration, and the actions performed. Cross-reference with KABIR's badge scan to confirm the impossible travel. Determine what authentication method was used for the anomalous session.

**Flag:** `NIGHTJAR{impossible_travel_kabir_amsterdam_0135_stolen_session_token}`

**Narrative Reward:** The Amsterdam session was not a brute-force login. It used a valid session token — the same token that was issued to KABIR when he authenticated via the Volunteer Portal at `23:45 IST` on September 30th. The token was extracted from KABIR's browser by the `Ethereal_Sync_Helper.exe` payload (which he installed on September 27th). The malware did not steal KABIR's password. It stole his active session token and replayed it from an infrastructure node in Amsterdam — part of the Curator's relay network.

The session performed three actions in 4 minutes:
1. Listed all ceremony automation scripts
2. Downloaded the `ceremony-init.yml` configuration file (which contains the release controller's API endpoint)
3. Created a new API key for `nexus-svc-continuity` with admin scope

This is the moment the Curator's infrastructure obtained the API key that was later used to create the ghost volunteer record (VOL-127), the badge, and the certificate renewal request. KABIR's session token was the master key that opened every subsequent door.

**Hints:**
- **Level 1:** "If someone is scanned at a physical gate in India, they cannot be logging in from another continent at the same time. Look for geographic impossibilities."
- **Level 2:** "Filter the login log for sessions that originate from IP addresses outside the campus and VPN ranges. Cross-reference the timestamp with badge scan data."
- **Level 3:** "Session at 01:35:42 IST from IP 198.51.100.23 (Amsterdam, NL). KABIR was badge-scanned at Main Gate at 01:20 IST. The session used a stolen session token, not a password."

---

## Challenge 7.3 — The Badge That Approved Itself

**Points:** 25

**Technical Concept:** MFA fatigue, push notification abuse, and token misuse in a fictional context.

**Briefing:**
> KABIR's account has MFA enabled — a push notification to his registered device. Every login should require KABIR to approve a push notification on his phone. The Amsterdam session should have triggered an MFA prompt. It did — and it was approved.
>
> But KABIR did not approve it. The authentication log shows that between `01:30 IST` and `01:35 IST`, KABIR's device received **fourteen** MFA push notifications in rapid succession. This is a technique called **MFA fatigue** — the attacker repeatedly triggers authentication prompts until the target, exhausted and confused, approves one just to make them stop. Or until the system's rate limiter fails and a push is auto-approved after a timeout.
>
> In KABIR's case, it was the system. Push notification #14 was auto-approved by the NEXUS MFA gateway after a 30-second timeout — a "convenience feature" designed to prevent lockouts during festival operations. The gateway assumed that if 14 prompts were sent and none were explicitly denied, the user must be having a connectivity issue. It approved the request automatically.

**Task:** Examine the MFA bypass evidence (`mfa_bypass.html`). Identify the sequence of push notifications, the rate at which they were sent, the point at which KABIR explicitly denied a push, and the final auto-approval event. Determine the MFA gateway's timeout policy and explain why it approved a request that KABIR never explicitly accepted.

**Flag:** `NIGHTJAR{mfa_fatigue_14_pushes_auto_approve_30s_timeout_gateway}`

**Narrative Reward:** The MFA push timeline:
- `01:30:00` — Push #1 sent. KABIR: no response (asleep or away from phone).
- `01:30:45` — Push #2 sent. No response.
- `01:31:15` — Push #3 sent. No response.
- `01:31:30` — Push #4 sent. No response.
- `01:31:45` — Push #5 sent. No response.
- `01:32:00` — Push #6 sent. **KABIR: DENIED** (woke up, saw the notification, explicitly denied it).
- `01:32:15` — Push #7 sent. **KABIR: DENIED** (denied again).
- `01:32:30` — Push #8 sent. **KABIR: DENIED** (denied a third time).
- `01:33:00` — Push #9 sent. No response (KABIR stopped checking, assumed it was a system glitch).
- `01:33:30` — Push #10 sent. No response.
- `01:34:00` — Push #11 sent. No response.
- `01:34:20` — Push #12 sent. No response.
- `01:34:40` — Push #13 sent. No response.
- `01:35:10` — Push #14 sent. **AUTO-APPROVED** by MFA gateway after 30-second timeout.
- `01:35:42` — Session authenticated from Amsterdam IP.

The critical flaw: the NEXUS MFA gateway's timeout policy treated a sequence of unanswered pushes (after explicit denials) as a connectivity issue, not as an attack. The auto-approval was a "convenience feature" that prioritised availability over security. KABIR did the right thing — he denied the pushes. The *system* approved the login anyway.

**Hints:**
- **Level 1:** "MFA is not unbreakable. What happens when someone sends dozens of authentication prompts in a row? What happens when the MFA system has a 'convenience' timeout?"
- **Level 2:** "Count the push notifications in the timeline. Look for the ones KABIR explicitly denied. Then look for the one that was approved without his input. What mechanism approved it?"
- **Level 3:** "14 push notifications between 01:30 and 01:35. KABIR denied pushes #6, #7, and #8. Push #14 was AUTO-APPROVED by the MFA gateway after a 30-second timeout."

---

## Challenge 7.4 — The Person Who Was Never There

**Points:** 25

**Technical Concept:** Identity correlation and distinguishing a human from an account.

**Briefing:**
> The investigation has identified multiple identities: `kabir.mehra` (human), `kite-backup` (account), `nexus-svc-continuity` (service account), `maint_nexus_portal` (service account), `curator_404` (unknown), and `VOL-127 / NEXUS Infrastructure — Automated` (ghost volunteer). Some of these are people. Some are automated services. And one is a replayed persona — an identity that acts like a person but is entirely synthesised from stolen credentials and session data.
>
> The question is not which accounts were compromised. The question is which identity in the evidence is a person, which is a service, and which is a persona that was never real. The attacker did not just use multiple accounts. The attacker created the illusion of a human insider — a pattern of activity that looks like a person making decisions, when in reality every "decision" was an automated script executing a predefined sequence.

**Task:** Examine the identity graph (`identity_graph.html`). For each identity in the evidence, classify it as: **HUMAN** (a real person who performed real actions), **SERVICE** (a system account performing automated functions), or **PERSONA** (an identity constructed from stolen credentials to simulate a human). Identify the one identity that was specifically constructed to make the investigation believe a human insider was responsible.

**Flag:** `NIGHTJAR{persona_kite_backup_simulated_insider_from_stolen_creds}`

**Narrative Reward:** The identity classification:

| Identity | Type | Evidence |
|----------|------|----------|
| `kabir.mehra` | **HUMAN** | Real logins from campus/VPN, badge scans, ticket submissions, real work patterns. Made a mistake (clicked a phishing file) but performed no malicious actions. |
| `rhea.dsouza` | **HUMAN** | Database schema design, security reviews, internal memos. Designed the vulnerable trust architecture but raised warnings. |
| `nexus-svc-continuity` | **SERVICE** | Created during AETHER CORE development. Performs automated continuity tasks. Was hijacked but is not malicious by design. |
| `maint_nexus_portal` | **SERVICE** | Hardcoded maintenance account. Limited to certificate renewal. Used by MIRA-7 but created by developers. |
| `curator_404` | **HUMAN** | Aman Vyas's public persona. Posted teaser content, operated relay infrastructure. Real person with real intent. |
| `VOL-127 / NEXUS Infrastructure` | **SERVICE** | Ghost volunteer record created by API. No human exists behind this identity. |
| `kite-backup` | **PERSONA** ⚠ | Created on AETHER-7 by `nexus-svc-continuity`. Named to implicate KABIR. Used KABIR's credential pattern (SSH key comment format, account naming convention). Authenticated via token delegation, not a real login. Every action attributed to `kite-backup` was performed by an automated script mimicking KABIR's operational patterns. This identity was specifically designed to make investigators conclude that KABIR was the insider. |

The `kite-backup` persona is the false victim's shadow. It was constructed to look like KABIR created a backup account for himself — a common pattern for insider threats. But the account was created by a service account, authenticated by a token, and operated by a script. No human ever typed a command as `kite-backup`. It is an identity constructed from stolen patterns to simulate a guilty human.

**KABIR's message (displayed after solving):**
> *"I clicked it because I was trying to save the festival. I was behind on the ceremony scripts. The message looked like help. The tool looked like what I needed. I did not stop to check the sender domain because the tech review was in twelve hours and nothing was working. Do not blame the person who made the deadline. Blame the system that let one click become everything."*

**Transition:** The file that KABIR downloaded — `Ethereal_Sync_Helper.exe` — is now quarantined and available as a safe, non-functional sample for Room 8.

**Hints:**
- **Level 1:** "Not every account represents a person. Some are services. One is something else entirely — an identity that *pretends* to be a person. Which account was created specifically to look like a human insider?"
- **Level 2:** "Compare how each identity authenticated. Humans use passwords and SSH keys. Services use tokens. What authentication method did `kite-backup` use? Was it ever used by a real human?"
- **Level 3:** "`kite-backup` was created by `nexus-svc-continuity`, authenticated via `pam_nexus_token.so`, and named to match KABIR's patterns. It is a PERSONA — an identity constructed to simulate an insider."

---

## Room Transition

After solving Challenge 7.4, the following transmission appears:

> **SPECTRE CONTROL // 01:47 IST**
>
> Commander Ila Sen, quietly:
> *"KABIR clicked a file. That is his mistake, and it is a human one. But the Curator did not leave it to chance. He studied the festival's schedule, read KABIR's support tickets, matched the timing to a real deadline, and sent a message that was engineered to feel like help. Then he used KABIR's stolen session to build an entire fake insider — an account, a name, a key, and a trail of evidence that pointed straight at the one person who was trying the hardest to make the festival work."*
>
> *"I want to be angry at KABIR. But I am angry at a system that let one phishing email turn into a service account, a certificate, a trust chain, and control of the opening ceremony. The social engineering was brilliant. The technology that amplified it was our own."*
>
> Rhea:
> *"The file KABIR downloaded is still in quarantine. It is called Ethereal_Sync_Helper.exe. It looks like a small festival utility. It is not. And what it contains is the last piece of the puzzle — the mechanism that connects the Curator's phishing campaign to MIRA-7's autonomous propagation."*
>
> **Proceed to Room 8 — The Ghost in the Machine.**

---

## Connection to Room 1

- The **`curator_404` handle** from Room 1 is now confirmed as Aman Vyas's operational persona
- The **Parallax Systems** identifier from Room 1 appears in the phishing message's download domain (`cdn-nexus.parallax-sys.net`)

## Connection to Room 4

- The **`kite-backup` account** from Room 4 is now confirmed as a PERSONA, not a legitimate backup account
- The **`pam_nexus_token.so` authentication** from Room 4 is the mechanism that allowed the persona to operate without a real human
- The **token-based session** from Room 4 was created using the same stolen session token identified in Challenge 7.2

## Connection to Room 5

- The **API key** created during the stolen Amsterdam session was used to access the Volunteer Portal's administrative functions
- The **ghost volunteer record** (VOL-127) was created using this API key

## Connection to Room 6

- The **trust relationships** stolen from the certificate trust store were accessed using the API key obtained from KABIR's stolen session
- The **badge cloning** was enabled by the session token compromise

## Connection to Room 8

- The **`Ethereal_Sync_Helper.exe`** file is the malware sample that Room 8 will examine
- The **phishing delivery mechanism** provides context for the malware's packaging and social engineering wrapper
- The **session token theft** is one of the malware's functions that Room 8 will identify through static analysis

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room should be solvable in 15–20 minutes by participants with an understanding of social engineering concepts.
- The evidence files are portal-native — no external tools or live applications are required.
- No real credentials, email addresses, or phishing techniques that could be directly replicated are included. All content is **entirely fictional**.
- This room is emotionally important: it is the moment the story shifts from "who attacked us" to "how did the attack exploit human trust." KABIR's message should make participants feel empathy, not contempt.
- The MFA fatigue challenge teaches a real-world lesson: convenience features in authentication systems can become attack vectors.
- The identity graph challenge is the narrative climax of Act II — teams should feel the weight of understanding that the "insider" was manufactured.
