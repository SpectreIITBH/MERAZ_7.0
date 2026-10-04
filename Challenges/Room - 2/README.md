# Room 2 — The Dead Telegram

## Domain: Cryptography, Encoding, Hashes, and Steganography

---

## 🔊 Opening Transmission

> **NEXUS RELAY // 23:44 IST**
>
> *"The page is not the attack. It is a doorbell. Decode what came with it."*
>
> — **Rhea D'Souza**, NEXUS Engineer

---

## Story Context

`curator_404` sent a direct message to Kabir "Kite" Mehra — the Festival Technical Lead — asking him to "restore the old route." Attached to the message was a cipher capsule: an encrypted package containing four layered transmissions.

The capsule was intercepted by NEXUS's internal message logger before the system went offline. The messages are damaged, encoded, or deliberately obscured. But they carry critical intelligence about the breach.

Something in these messages names the next target. Something else proves the signature on a trusted message was forged. And buried in what looks like noise, a single sentence will change who the team suspects.

**Decode the capsule. Find the name beneath the code.**

---

## Room Mood

An old internal chat terminal. Messages arrive with timestamps in the future and disappear after being opened. The Curator's messages sound like a dramatic villain, while the system logs keep exposing that the "unhackable" chat is a badly configured service. The mood is cryptic but slightly absurd — the most dangerous message in the system was sent over a chat client that stores passwords in plaintext.

---

## Evidence Files

| File | Description |
|------|-------------|
| `evidence/cipher_capsule.html` | The intercepted message capsule with 4 encoded transmissions |
| `evidence/hash_verification.html` | A set of files with their hashes for verification |
| `evidence/hidden_image.html` | An image containing a steganographic message |
| `evidence/signed_messages.html` | Four signed messages — one has been tampered with |

---

## Challenge 2.1 — The Message That Looks Like Noise

**Points:** 25

**Technical Concept:** Base64 encoding, XOR operations, and classical cipher detection.

**Briefing:**
> The first transmission in the capsule is a block of text that looks like random garbage. But the Curator doesn't waste bandwidth. This is a message — it just doesn't want to be read by anyone watching the wire. Identify the encoding, decode it, and read what the Curator wanted Kabir to know.

**Task:** Open the cipher capsule (`cipher_capsule.html`) and examine Transmission 1. The message is multi-layered: first Base64, then a Caesar cipher (shift 13, i.e., ROT13). Decode both layers to reveal the plaintext.

**Flag:** `NIGHTJAR{the_host_with_the_blue_name_is_lying}`

**Narrative Reward:** The decoded message reads: *"THE HOST WITH THE BLUE NAME IS LYING. DO NOT TRUST THE STATUS PAGE. THE REAL CONTROLLER IS UNDERNEATH. — C"* This is the Curator warning Kabir that the NEXUS system status is being spoofed — the "blue name" refers to a host alias in the network that will appear in Room 3.

**Hints:**
- **Level 1:** "The Curator's messages always hide in layers. Start by identifying what kind of encoding uses only letters, numbers, plus, slash, and equals."
- **Level 2:** "The outer layer is Base64. Decode it first. The result will still look encoded — try a simple letter-shift cipher."
- **Level 3:** "Base64 decode, then apply ROT13 (Caesar cipher with shift 13)."

---

## Challenge 2.2 — The Hash That Is a Door

**Points:** 25

**Technical Concept:** Hash recognition (MD5, SHA-1, SHA-256), hash verification, and file integrity.

**Briefing:**
> The second transmission contains no readable text — only a hash. The Curator says: *"Match the door to open it."* Five files were recovered from the NEXUS backup. One of them matches the hash. The matching file contains the next clue. But remember: a hash identifies data, not guilt or intent. The file that matches is evidence, not a confession.

**Task:** Open the hash verification page (`hash_verification.html`). You're given one target hash and five candidate files. Calculate or compare the hashes to find the matching file, then read its contents for the next piece of intelligence.

**Flag:** `NIGHTJAR{blue_name_is_host_alias_not_a_person}`

**Narrative Reward:** The matching file reveals: *"The blue name is not a person. It is a host alias. NEXUS assigned colour-coded names to its internal relays during testing. BLUE was the relay that handled volunteer authentication. It was renamed before production — but the old alias still resolves."* This means the "blue name" from Challenge 2.1 is a machine, not a human — a crucial distinction for Room 3.

**Hints:**
- **Level 1:** "A hash is a fingerprint. Match the fingerprint to find the right file."
- **Level 2:** "Look at the hash length. 64 hex characters = SHA-256. Compare each file's hash against the target."
- **Level 3:** "File C (`relay_config_backup.log`) matches the target hash."

---

## Challenge 2.3 — The Image That Whispers

**Points:** 25

**Technical Concept:** Steganography — hidden data in visual media.

**Briefing:**
> The third transmission is an image. It looks like a NEXUS system architecture diagram — the kind Rhea would share in an engineering review. But the Curator attached it with a note: *"The diagram tells you what to build. The whisper tells you who never signs in."* There is a message hidden inside the image data.

**Task:** Examine the image (`hidden_image.html`). The hidden message is encoded using a visual steganography technique — look for data hidden in pixel patterns, least-significant bits, colour channel anomalies, or text embedded in non-visible layers.

**Flag:** `NIGHTJAR{ask_the_person_who_never_signs_in}`

**Narrative Reward:** The hidden message reads: *"ASK THE PERSON WHO NEVER SIGNS IN."* This refers to a service account — an automated identity that authenticates to NEXUS systems but has no human behind it. This service account will become critical in Room 6 (The Living Ledger) when teams discover that the attacker used trust relationships, not stolen passwords.

**Hints:**
- **Level 1:** "Not everything visible is everything present. The image contains more than architecture."
- **Level 2:** "Look at the image source code. The steganographic message may be embedded as data attributes, hidden text, or encoded in the visual pattern."
- **Level 3:** "The message is hidden as zero-width characters or as text in the image's data layer. Look for the phrase 'ASK THE PERSON'."

---

## Challenge 2.4 — The Dead Message

**Points:** 25

**Technical Concept:** Digital signatures, message integrity, and tamper detection.

**Briefing:**
> Four signed messages were recovered from the NEXUS internal messaging system. Three are authentic. One has been altered after it was signed — its content no longer matches its signature. Find the tampered message. The altered content contains the name of the next relay in the attack chain.

**Task:** Open the signed messages page (`signed_messages.html`). Each message has a sender, timestamp, content, and a cryptographic signature. One message's content has been changed after signing — the signature no longer validates. Identify which message was tampered with and extract the hidden relay name from its altered content.

**Flag:** `NIGHTJAR{aether_7_relay_compromised}`

**Narrative Reward:** The tampered message was originally signed by "Rhea" — but the timestamp predates her employment at NEXUS by two months. The altered content contains the relay name `AETHER-7`. This is the next node in the attack chain. The Curator modified Rhea's old test message to point teams toward the compromised relay — whether as a genuine lead or a manipulation remains unclear.

**Twist micro-beat:** Players are told: *"Do not trust the signature yet. You need context. The signer's identity will be verified in a later room."*

**Hints:**
- **Level 1:** "A valid signature means the message hasn't changed. An invalid signature means someone altered the content after it was signed."
- **Level 2:** "Compare each message's stated signature hash with what the content should produce. One won't match."
- **Level 3:** "Message 3, signed by 'Rhea', has a mismatched signature. Its content now says 'AETHER-7' — but the original message was different."

---

## Room Transition

After solving Challenge 2.4, the following transmission appears:

> **NEXUS RELAY LOG // 00:02 IST**
>
> The cipher capsule has been decoded. The four transmissions point to a single destination: **AETHER-7**, a network relay that should have been decommissioned months ago.
>
> Rhea's engineering notes confirm: *"AETHER-7 was the test relay for the continuity module. It was supposed to be air-gapped after testing. Someone reconnected it."*
>
> A packet capture from AETHER-7's last 30 minutes of activity has been recovered from the backup system. The relay is sending a small, regular packet every 43 seconds. To something. Or someone.
>
> **Proceed to Room 3 to analyse the network capture.**

---

## Connection to Room 1

- The Curator's handle `curator_404` (discovered in Room 1) is the sender of the cipher capsule
- The `Parallax Systems` name (from Room 1's metadata) reappears in the signed messages
- The phrase "Nothing stays local" (from AETHER/07 in Room 1) is referenced in one of the transmissions
- The mirror domain `nexus-meraz.festival.in.net` (from Room 1) appears in the hash verification files

## Connection to Room 3

- The relay name `AETHER-7` is the network node whose packet capture forms Room 3
- The "host with the blue name" is a machine that will appear in the PCAP
- The "person who never signs in" is a service account that communicates through the relay
- The forged Rhea signature foreshadows the trust-relationship exploit in later rooms

---

## Admin Notes

- All flags follow the format `NIGHTJAR{...}` with lowercase, underscores, and no spaces.
- This room should be solvable in 10–15 minutes by participants with basic crypto knowledge.
- No external tools are strictly required — all decoding can be done with browser tools or CyberChef.
- The steganography challenge uses accessible techniques (not deep LSB extraction requiring specialised software).
- All content is **entirely fictional**.
