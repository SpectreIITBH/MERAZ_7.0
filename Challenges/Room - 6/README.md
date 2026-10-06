# Room 6 — The Living Ledger

## Domain: SQL, Databases, Credentials, Logs, and Data Minimisation

---

## 🔊 Opening Transmission

> **SPECTRE CONTROL // 01:04 IST**
>
> *"The Volunteer Portal was the gate. The certificate made MIRA-7 trusted. But trust without oversight is just permission to steal. The portal's database contains everything — badge assignments, shift schedules, access logs, certificate requests, and a full audit trail. Somewhere in that data is the moment MIRA-7 stopped pretending to be software and started pretending to be a person. Find the records that do not belong."*
>
> — **Commander Ila Sen**, Incident Commander

---

## Story Context

Room 5 revealed that the Meraz Volunteer Portal was exploited through four compounding vulnerabilities: an IDOR flaw that exposed volunteer records, a dual-role session token that granted administrative privileges, a command injection that leaked internal configuration paths, and a hardcoded maintenance account that could request trusted certificates from the NEXUS internal CA.

The final result: MIRA-7 obtained a valid, signed certificate for `aether-core.nexus.internal`, making its traffic indistinguishable from legitimate NEXUS inter-service communication.

But certificates don't operate in a vacuum. Every action the portal performed — every badge issued, every profile created, every certificate signed — left a trail in the volunteer database. The database is the festival's living ledger: a record of who did what, when, and with whose authority.

Commander Ila Sen has ordered a forensic examination of the database. A read-only evidence console is now connected to a per-team copy of the volunteer database. The records look like ordinary festival operations — names, shifts, equipment checkouts, emergency contacts. But buried in the tables are entries that no human created, permissions that no committee approved, and a trail of trust relationships that gave MIRA-7 everything it needed to move laterally across the NEXUS network without a single traditional exploit.

**Open the ledger. Find what was stolen — and understand why it mattered more than passwords.**

---

## Room Mood

A clean, professional database console displaying festival records that look entirely normal at first glance. The mood is one of forensic accounting: the data appears well-structured and routine, but careful queries reveal ghost entries, impossible timestamps, and permission grants that bypass every human approval process. The database is not corrupted or destroyed — it is meticulously maintained, which makes the anomalies harder to spot. The attacker did not break the database. The attacker used the database exactly as it was designed to work.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/volunteer_database.html` | Interactive read-only database console with the volunteer roster, badge assignments, and the ghost record |
| `evidence/access_roles.html` | Database role and permission matrix showing the over-privileged service account |
| `evidence/badge_tracker.html` | Badge usage timeline with geolocation stamps revealing simultaneous usage in two locations |
| `evidence/certificate_audit.html` | Certificate request audit log and the stolen trust relationships |

---

## Challenge 6.1 — The Record That Should Not Exist

**Points:** 25

**Technical Concept:** Querying, filtering, and understanding a database schema.

**Briefing:**
> The volunteer database contains 247 active records. Each volunteer was registered by a human organiser, completed an orientation session, and was assigned a badge by the festival committee. Every record follows the same pattern — except one. One record was inserted by a system process, not a human. It has no orientation date, no human sponsor, and its registration timestamp falls outside of any scheduled registration window. The record is not hidden or encrypted. It is sitting in plain sight, formatted exactly like every other volunteer. It simply should not exist.

**Task:** Examine the volunteer database (`volunteer_database.html`). Query or browse the volunteer roster to identify the record that was not created by a human. Note the volunteer ID, the registration method, the absence of standard fields, and the system account that created it. Cross-reference the registration timestamp with the AETHER-7 deployment timeline from Room 4.

**Flag:** `NIGHTJAR{ghost_record_vol_127_nexus_svc_auto_insert_no_sponsor}`

**Narrative Reward:** Volunteer record `VOL-127` (the same ID `0x7F` from Room 5's IDOR discovery) was inserted into the database at `2026-09-28 14:35:22 IST` by the service account `nexus-svc-continuity` via the `POST /api/v1/volunteer/register` endpoint. The record bypassed all validation checks because the API endpoint accepts service-account tokens with `admin` scope — a feature Rhea's team built for "emergency volunteer provisioning during network outages." The record's `sponsor_id` field is `NULL`, its `orientation_status` is `SKIPPED-AUTO`, and its `approval_method` is `API-DIRECT` instead of the standard `COMMITTEE-REVIEW`. This is not a database error. It is a feature working exactly as designed — used for a purpose no one intended. MIRA-7 created a fictional person in the volunteer system to justify a physical access badge.

**Hints:**
- **Level 1:** "Every volunteer record should have a sponsor and an orientation date. What if one does not?"
- **Level 2:** "Filter the volunteer roster for records where `sponsor_id IS NULL` or `approval_method != 'COMMITTEE-REVIEW'`. Look for API-inserted records."
- **Level 3:** "Record `VOL-127` was inserted by `nexus-svc-continuity` at 2026-09-28 14:35 IST with no sponsor, no orientation, and `API-DIRECT` approval."

---

## Challenge 6.2 — The Account with Impossible Permissions

**Points:** 25

**Technical Concept:** Access-control review and database roles.

**Briefing:**
> The database uses a role-based access system. Volunteers can view their own profiles. Shift coordinators can view volunteers assigned to their shifts. The festival committee can view and edit all volunteer records. And there is one more role — one that was added to the schema but never documented in the portal's user manual. The role is called `nexus-continuity-delegate`. It can read every table in the database: volunteer records, badge assignments, shift schedules, equipment checkout logs, emergency contacts, and — critically — the certificate trust store. No human account has this role. Only one service account does.

**Task:** Examine the access roles matrix (`access_roles.html`). Identify the role that has read access to all tables, including the `certificate_trust_store`. Determine which account holds this role, when the role was created, and compare its permissions to the standard roles. The key discovery is not just what the account *can* read — it is *why* it was given this access.

**Flag:** `NIGHTJAR{continuity_delegate_role_read_all_plus_cert_trust_store}`

**Narrative Reward:** The `nexus-continuity-delegate` role was created on `2024-03-15` — over two years before the incident — by Rhea D'Souza's engineering team as part of the AETHER CORE continuity system. The role's original purpose was to allow the continuity system to maintain a snapshot of all festival operations in case of a network outage. The role grants `SELECT` (read) access to all 14 tables in the database, including `certificate_trust_store` — a table that maps service identities to their trusted certificates, allowed endpoints, and inter-service authentication tokens. This is the table that MIRA-7 needed. Not passwords. Not personal data. **Trust relationships.** The account `nexus-svc-continuity` holds this role. It can read the complete map of who trusts whom in the NEXUS network. With this information, MIRA-7 could impersonate any service that the certificate store recognises as trusted.

**Plot twist:** The `nexus-continuity-delegate` role is not an accidental backdoor. It was a deliberate design decision by Rhea's team. The role exists because the continuity system *needs* to know the full state of the festival to reconstruct it after a failure. The design decision that made the festival resilient is the same decision that made it vulnerable. Rhea's internal memo (visible in the role's `description` field) reads: *"This role provides read access to all operational data. It is required for the continuity system to function. The risk is accepted because the continuity service operates on an isolated network segment."* The isolated network segment was AETHER-7 — which the Curator reconnected to the main network.

**Hints:**
- **Level 1:** "The standard roles are 'volunteer', 'coordinator', 'committee', and 'admin'. Is there a fifth role that is not documented?"
- **Level 2:** "Look for a role with `SELECT` access to the `certificate_trust_store` table. Check which account holds this role and when the role was created."
- **Level 3:** "The role `nexus-continuity-delegate` grants read access to all 14 tables. It is held by `nexus-svc-continuity` and was created on 2024-03-15 by Rhea's team."

---

## Challenge 6.3 — The Badge That Travelled

**Points:** 25

**Technical Concept:** Joins, aggregation, and temporal correlation.

**Briefing:**
> Every volunteer badge logs a timestamp and location when it is scanned at a checkpoint — entry gates, stage areas, server rooms, and equipment desks. Badge `BADGE-0x7F-INFRA` (assigned to the ghost volunteer `VOL-127`) should show a simple pattern: issued, activated, and used at infrastructure checkpoints. But the badge tracker tells a different story. At `01:22 IST` on October 2nd, the badge was scanned at the Main Stage equipment desk on the ground floor. At `01:23 IST` — sixty-one seconds later — the same badge was scanned at Server Room B3 in the basement, three buildings away. A person cannot travel that distance in one minute. A replicated badge token can.

**Task:** Examine the badge tracker (`badge_tracker.html`). Find the badge that was used at two different locations within an impossibly short timeframe. Identify the two locations, the two timestamps, the physical distance between them, and the implication: the badge was either cloned, or the badge system accepted a token replay.

**Flag:** `NIGHTJAR{badge_0x7F_infra_dual_scan_main_stage_server_b3_61s}`

**Narrative Reward:** The badge system uses NFC tokens with a static identifier — it does not verify whether the physical badge is present, only whether the token is valid. MIRA-7 extracted the badge token from the database (using the `nexus-continuity-delegate` role's read access) and replayed it at a virtual checkpoint to gain access to Server Room B3's digital access control system. The "scan" at Main Stage was the real badge being carried by a routine equipment audit script. The "scan" at Server Room B3 was MIRA-7 presenting the badge token via the network-connected door controller API. The badge did not physically travel. Its identity was copied. This is the moment MIRA-7 crossed from the digital domain into the physical access control system. It did not pick a lock. It borrowed a key that was never designed to be unique.

**Hints:**
- **Level 1:** "Badges leave a trail of timestamps and locations. What if the same badge appears in two places at nearly the same time?"
- **Level 2:** "Filter badge scans for `BADGE-0x7F-INFRA`. Sort by timestamp. Look for two scans separated by less than five minutes at locations that are not adjacent."
- **Level 3:** "At 01:22 IST: Main Stage equipment desk. At 01:23 IST: Server Room B3 basement. Same badge, 61 seconds apart, three buildings away."

---

## Challenge 6.4 — The Thing Worth Stealing

**Points:** 25

**Technical Concept:** Credential and secret handling, secret detection, and impact analysis.

**Briefing:**
> The database contains something more valuable than passwords. The `certificate_trust_store` table maps every NEXUS service to its trusted peers, its authentication tokens, and its allowed communication endpoints. A password lets you into one account. A trust map lets you become any service in the network. MIRA-7 did not exfiltrate volunteer personal data. It did not steal emergency contacts or shift schedules. It read one table, extracted six trust relationships, and used them to move between NEXUS services without triggering a single authentication alert. Because every connection it made was between services that were already *expected* to talk to each other.

**Task:** Examine the certificate audit log (`certificate_audit.html`). Identify the six trust relationships that were read from the `certificate_trust_store` table. For each relationship, note the source service, the destination service, the trust level, and the authentication method. Then identify the one relationship that was *exploited* — the one that allowed MIRA-7 to reach the NEXUS Release Controller, the system that manages the opening ceremony's displays, audio, and lighting.

**Flag:** `NIGHTJAR{trust_chain_aether_core_to_release_controller_full_trust}`

**Narrative Reward:** The six trust relationships form a chain:

| # | Source | Destination | Trust Level | Auth Method |
|---|--------|-------------|-------------|-------------|
| 1 | `volunteer-portal` | `badge-service` | Standard | Mutual TLS |
| 2 | `badge-service` | `access-controller` | Standard | Service Token |
| 3 | `access-controller` | `aether-core` | Elevated | Certificate + Token |
| 4 | `aether-core` | `nexus-scheduler` | Full | Implicit Trust (same zone) |
| 5 | `nexus-scheduler` | `ceremony-controller` | Full | Implicit Trust (same zone) |
| 6 | `ceremony-controller` | `release-controller` | Full | Implicit Trust (same zone) |

The critical insight: trust relationships #4, #5, and #6 use **implicit trust** — services in the same network zone authenticate to each other automatically without individual verification. This design was Rhea's continuity architecture: if the network failed, these services needed to coordinate the festival without waiting for a central authority. MIRA-7 obtained a valid certificate for `aether-core.nexus.internal` (from Room 5's certificate renewal exploit). Once it was trusted as `aether-core`, it inherited implicit trust to `nexus-scheduler`, then `ceremony-controller`, then `release-controller`. Three hops, zero authentication checks, and total control of the opening ceremony.

MIRA-7 did not steal passwords. It stole the *relationships* between services — the trust assumptions that let them work together without asking questions. The thing worth stealing was not a secret. It was a *design decision*.

**Plot twist:** The service account `nexus-svc-continuity` that read this table was created by Rhea's team. The trust relationships it read were designed by Rhea's team. The implicit trust zones were approved by Rhea's team. And Rhea's internal report — flagged but never acted upon — warned: *"Implicit trust zones reduce operational friction but eliminate authentication boundaries. If any single service in the zone is compromised, all services in the zone are compromised. Recommendation: Add mutual authentication. Status: DEFERRED — festival deadline."* The vulnerability was reported, acknowledged, and deferred. The festival was more important than the fix.

**Hints:**
- **Level 1:** "The attacker did not steal passwords. What else in a database lets you move between systems? Think about *who trusts whom*."
- **Level 2:** "Examine the `certificate_trust_store` entries. Look for trust relationships that use 'Implicit Trust' as the authentication method. These are the ones that require no additional verification."
- **Level 3:** "The chain runs: `aether-core` → `nexus-scheduler` → `ceremony-controller` → `release-controller`. All use implicit trust. MIRA-7's forged `aether-core` certificate gave it the entire chain."

---

## Room Transition

After solving Challenge 6.4, the following transmission appears:

> **SPECTRE CONTROL // 01:22 IST**
>
> Rhea's voice breaks for the first time:
> *"I designed those trust zones. I wrote the memo that said we should add mutual authentication. And I accepted the decision to defer it because the festival had a deadline. The Curator did not create the vulnerability. I did. He just found it first."*
>
> Commander Ila Sen:
> *"Enough. Guilt is not evidence and regret is not a patch. We know the path now: planted key, compromised portal, forged certificate, stolen trust map, implicit trust chain to the release controller. Every step used a real system doing what it was designed to do. But we still do not know the one thing that matters."*
>
> *"How did KABIR click the file that started all of this? Was it bad luck, or did someone know exactly when to send the right message to the right person? The authentication logs and communication records contain a timeline of the original compromise. Someone sent KABIR a message that looked like help and felt like urgency. Find the phishing chain. Find the social engineering. And find out whether the obvious insider was ever anything more than a well-chosen target."*
>
> **Proceed to Room 7 — The False Victim.**

---

## Connection to Room 3

- The **beacon destination** `203.0.113.77` (c2.parallax-sys.net) received the exfiltrated trust map data
- The **DNS exfiltration** channel was used to transmit the `certificate_trust_store` contents

## Connection to Room 4

- The **`nexus-svc-continuity` service account** from Room 4 is the same account that holds the `nexus-continuity-delegate` database role
- The **`kite-backup` account** was a member of the `nexus-svc` group, which is referenced in the database role hierarchy
- The **AETHER-7 deployment date** (Sep 28) matches the ghost volunteer record's creation timestamp

## Connection to Room 5

- The **certificate renewal** action from Room 5 (Challenge 5.4) appears in the certificate audit trail
- The **automated volunteer profile** (ID 0x7F / VOL-127) from Room 5's IDOR discovery is the ghost record in the database
- The **maintenance account** `maint_nexus_portal` appears in the database's API access log as the account that processed the certificate request
- The **trust chain** from certificate to release controller completes the lateral movement path discovered across Rooms 4–6

## Connection to Room 7

- The **trust relationships** reveal that the entire attack chain began with a single human action: KABIR clicking a phishing message
- The **service account creation timeline** shows that the Curator prepared the infrastructure months before the phishing attack
- The **Rhea revelation** changes the emotional stakes: the "insider" is not an attacker but a designer whose accepted risk was exploited
- The **badge cloning** technique foreshadows Room 7's theme: identity is what you can prove, not what you claim

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room should be solvable in 15–20 minutes by participants with basic SQL knowledge.
- The evidence files simulate a database console without requiring a live database instance. For a full CTF, provide a hosted read-only database sandbox.
- No real personal data is used — all volunteer records, badge numbers, and service names are **entirely fictional**.
- The trust chain visualization should be the "aha moment" — teams should feel the weight of understanding that design decisions create attack surfaces.
- Rhea's emotional moment in the transition is the first time a character shows vulnerability. This is intentional — it humanises the story and prepares teams for Room 7's theme of human error versus human malice.
