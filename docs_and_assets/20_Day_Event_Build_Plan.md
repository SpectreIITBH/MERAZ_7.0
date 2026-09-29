# SPECTRE x Meraz: 20-Day Developer Plan

## Project Definition

**Goal:** Integrate a playable, gamified cybersecurity event experience into the existing event website within 20 days.

**What remains:** Platform implementation and integration. The room/challenge concepts and story are already documented in [Proposed_Story_Plan - 1.md](Proposed_Story_Plan%20-%201.md); do not schedule new challenge authoring. Treat the source document and existing challenge assets as inputs. Verify, map, import, and test them.

**Player loop:** Event entry/team identity -> incident briefing -> mission map -> room -> challenge -> solve in the labeled location -> submit answer -> immediate result/points/progress -> room unlock and story/NPC update.

Gamification must support the player's next action, not just decorate the site: clear objectives, visible progress, meaningful solve feedback, points, room unlocks, and story context. Harsha designs the story NPC and visual direction for this game layer; Jagath implements the UI with Harsha's assets/specification.

## Assumptions and Feasibility Gate

- There is an existing event website, and the team can access its repository, staging environment, and deployment process.
- Reuse existing sign-in/team identity. Do not build new authentication unless the Day 1 audit proves none is available and Akash approves the scope change.
- The existing challenge package, expected answers, points, hints, and evidence assets are available or their owner can supply them by Day 2.
- Launch does not depend on custom VMs, live vulnerable services, realtime sockets, or a new cloud platform. Follow each challenge's existing solve location: browser tasks stay in the portal; file tasks are solved locally and submitted on the portal.
- If repository, staging, or deployment access is unavailable by midday Day 1, Akash escalates that as a schedule blocker. Do not assume a greenfield replacement can be completed in the remaining time.

## Team and Workstream Ownership

| Owner | Accountable workstream | Main deliverables |
| --- | --- | --- |
| Akash | Product owner and release decisions | Scope, acceptance criteria, decisions, stakeholder access, go/no-go |
| Jagath | Frontend and existing-site integration | Routes, mission map, room/challenge UI, responsive implementation |
| Bhavya | QA and release quality | Test plan, functional/security checks, defect triage, retest evidence |
| Kushal | Challenge data and asset integration | Import manifest, stable IDs, evidence links, content/config validation |
| Aryamaan | Story integration | Room/story mapping, reveal order, NPC dialogue placement, source consistency |
| Jashwanth Kumar (B26MM021) | Backend and security | Data/API contracts, submissions, progress, scoring, unlocks, deployment |
| Ankit Gyen (B25CS006) | Organizer workflow and event operations | Admin workflow requirements, organizer console acceptance, support process |
| Rohit (B25CS046) | Rules, challenge verification, runbook | Existing answer-key mapping, independent solve verification, player rules/journey, support/admin runbook |
| Harsha | Game visual and NPC design | NPC character design, game visual direction, UI states/assets, implementation review |

Rohit is not assigned to create challenges: the challenge set already exists. He owns the event rules/player journey/runbook and verifies existing challenge-to-answer mappings. Ankit owns organizer-workflow acceptance; Rohit documents the operating procedure. Jashwanth has the hardest technical work, while frontend, QA, content integration, design, product, and operations have separate owners.

**Planning capacity:** About 2.5-3.5 focused hours per person per day; Jashwanth may take up to 4 hours for the hardest technical integration. Confirm actual availability on Day 1. If capacity is lower, remove optional features before cutting test or security time.

## Product Scope

### P0 - Required for launch

- Existing sign-in/team identity integration.
- Incident briefing and ten-room mission map with locked, available, active, and completed states.
- Reusable room and challenge views that render imported material.
- Solve-location label, evidence link/download, hint, answer submission, feedback, and points.
- Server-side answer validation, one-time solve/score recording, team-scoped progress, and server-enforced room unlocks.
- Basic scoreboard/progress view and permission-gated organizer controls for team lookup and challenge availability.
- Gamified feedback: objectives, progress indicators, meaningful solve feedback, room/NPC story updates, and completion state. Use purposeful motion; respect reduced-motion preferences.
- Responsive, keyboard-usable experience with clear loading, empty, success, and error states.

### P1 - Only after P0 is stable

Achievements/badges, branching NPC dialogue, live incident feed, realtime scoreboard, final-room VM, and optional story endings. No P1 feature may delay the P0 vertical slice, testing, or deployment.

## Technical Shape

Decide implementation details after the repository audit; follow the current stack rather than imposing a new one. Maintain these logical boundaries even if the existing app combines them:

1. **Player UI:** briefing, mission map, room/challenge views, submissions, progress, and score.
2. **Game service/API:** team-scoped room data, submission validation, solve recording, points, unlocks, hints, and organizer actions.
3. **Persistent data/config:** public room/challenge content, private answer material, submissions/solves, hint use, and event settings. Keep answers separate from public challenge responses.
4. **Organizer workflow:** authorized team lookup, challenge pause/availability, progress review, score-correction procedure, and announcement/support handoff if supported.
5. **Design assets:** NPC art and UI states from Harsha, integrated by Jagath with specified dimensions, formats, alt text, and fallback behavior.

**Data invariants:** stable room/challenge IDs; team-scoped progress; unique solve per team/challenge; score derived from accepted solves; server-enforced unlocks; no answers in frontend bundles, public API responses, or client logs. Record organizer score corrections with actor, reason, and timestamp where the existing platform supports it.

## Definition of Done

A feature is done when integrated into the existing website, reviewed by a second owner, passes its relevant test, works on mobile/keyboard where applicable, and has no known P0 defect. Each code/config change needs a linked task, reviewer, test evidence, and migration/config note where relevant. Bhavya keeps acceptance evidence; Jashwanth reviews backend/security; Jagath reviews frontend integration; Akash decides scope tradeoffs.

## 20-Day Implementation Schedule

### Day 1 - Repository audit and feasibility
- **Akash:** Confirm deadline, decision-makers, access owners, actual availability, event requirements, and release date; open decision/risk log.
- **Jagath:** Inspect frontend routes, styles, components, mobile behavior, staging entry point, and integration boundary.
- **Bhavya:** Define must-pass journeys: team entry, room/challenge open, wrong/correct submit, score/unlock, and organizer pause.
- **Kushal:** Locate the complete challenge package/assets; inventory IDs, solve types, files, points, hints, answer references, and missing inputs.
- **Aryamaan:** Map ten rooms, story text, transitions, and NPC appearances from the source plan.
- **Jashwanth:** Audit backend, identity, persistence, API, deployment, secrets, and tests; recommend the smallest compatible architecture and list blockers.
- **Ankit:** Inventory organizer actions and event-day failure scenarios; note which are already supported.
- **Rohit:** Gather final rules, scoring/hint policy, answer keys, and solve paths; create a private challenge-ID-to-answer map without changing answers.
- **Harsha:** Review NPC references and the current site's visual language; prepare a one-page NPC/game-design brief and asset requirements.
- **Gate:** By end of day, Akash accepts feasibility or records a blocker/scope cut. No greenfield rebuild is assumed.

### Day 2 - Product contract and technical design
- **Akash:** Approve P0/P1, team-entry model, scoring, unlock rules, and explicit exclusions.
- **Jagath:** Produce route map and low-fidelity layouts for dashboard, mission map, room, challenge, scoreboard, and organizer view.
- **Bhavya:** Convert P0 journeys into test cases with expected results and test-team fixtures.
- **Kushal:** Create import manifest for existing challenge records/assets with stable IDs and verification status.
- **Aryamaan:** Map source story to room intro, challenge context, post-solve/NPC update, and next-room reveal.
- **Jashwanth:** Agree API/data contracts and private-answer storage with Jagath; record an architecture decision.
- **Ankit:** Define organizer roles/permissions and acceptance flow for lookup, pause, progress review, and score correction.
- **Rohit:** Publish event rules/player-flow draft and answer-key custody procedure; map existing answers to challenge IDs.
- **Harsha:** Deliver NPC concept direction and game UI references, including map mood and character states.
- **Gate:** Approved scope, route/data contracts, import manifest, design direction, and test plan.

### Day 3 - App shell and first vertical slice setup
- **Akash:** Clear repository/staging permissions and external dependencies; approve the Day 2 architecture decision.
- **Jagath:** Add game entry route, shared page shell, navigation, and placeholder dashboard in the existing site.
- **Bhavya:** Set up test accounts/team fixtures and smoke-test instructions; verify baseline build.
- **Kushal:** Normalize first-room challenge records into the import format and validate asset paths.
- **Aryamaan:** Prepare approved story text for the first playable room and map an existing NPC message.
- **Jashwanth:** Implement minimal persistence/API skeleton and staging health check using the existing stack.
- **Ankit:** Turn organizer actions into acceptance criteria with expected permissions and recovery behavior.
- **Rohit:** Verify first-room IDs, answers, points, hints, and solve locations against the private source key.
- **Harsha:** Create first NPC concept sheet and asset handoff specification.
- **Gate:** Staging build runs; game route opens; first room is ready to render.

### Day 4 - Mission dashboard and room map
- **Akash:** Review dashboard against P0 and resolve product questions quickly; keep optional features out.
- **Jagath:** Implement dashboard and ten-room map with locked/available/active/completed states and responsive layout.
- **Bhavya:** Test room-state rendering, navigation, focus order, and narrow-screen layout.
- **Kushal:** Import metadata for Rooms 1-3; validate IDs, points, hints, file paths, and availability.
- **Aryamaan:** Verify Rooms 1-3 story order and identify NPC message placements.
- **Jashwanth:** Provide team-scoped room/progress data interface for the map.
- **Ankit:** Validate organizer-visible team/progress fields and role separation.
- **Rohit:** Reconcile Rooms 1-3 answer mappings; keep private values out of public content.
- **Harsha:** Review map direction and NPC portrait/art specs; check game-state readability.
- **Gate:** Room map displays real records and correct team state.

### Day 5 - Reusable room and challenge views
- **Akash:** Approve room/challenge hierarchy and player-facing rule placement.
- **Jagath:** Implement reusable room/challenge views: task, solve-location label, evidence, hint, answer input, feedback, and navigation.
- **Bhavya:** Test loading, empty, long text, download, hint, wrong answer, success, and error states.
- **Kushal:** Import metadata/assets for Rooms 4-6 and validate the import.
- **Aryamaan:** Verify Rooms 4-6 narrative placement and transitions against the source.
- **Jashwanth:** Implement challenge-detail API that returns public fields only and define safe submit responses.
- **Ankit:** Validate organizer workflow for inspecting and pausing a challenge.
- **Rohit:** Reconcile Rooms 4-6 answer references, points, hints, and solve locations.
- **Harsha:** Deliver first usable NPC asset(s), alt text, format/dimensions, and fallback; review challenge-page fit.
- **Gate:** Test team can navigate from map to a populated challenge page.

### Day 6 - Submission vertical slice
- **Akash:** Review vertical-slice criteria and approve answer-normalization rules.
- **Jagath:** Connect challenge page to detail/submission API; implement loading/error/success states.
- **Bhavya:** Test correct, incorrect, blank, malformed, and duplicate submissions.
- **Kushal:** Import metadata/assets for Rooms 7-10; check duplicate IDs and broken links.
- **Aryamaan:** Verify Rooms 7-10 story ordering and final-room setup.
- **Jashwanth:** Implement server-side flag validation and unique solve recording; keep private answers out of client responses.
- **Ankit:** Walk the player journey through the slice and confirm help/support is findable.
- **Rohit:** Independently solve the vertical-slice challenge and verify its platform key mapping.
- **Harsha:** Review NPC placement in the slice and submit prioritized visual feedback.
- **Gate:** One challenge works from team entry through server-validated solve and visible progress.

### Day 7 - Identity, persistence, and score integrity
- **Akash:** Confirm existing login/team behavior with the site owner; approve fallback only if necessary.
- **Jagath:** Handle signed-in, signed-out, expired-session, and return-to-challenge states.
- **Bhavya:** Test cross-team isolation with at least two test teams.
- **Kushal:** Reconcile all challenge metadata with the source manifest; fix references, not challenge design.
- **Aryamaan:** Check room/story content selection and behavior after refresh/navigation.
- **Jashwanth:** Persist team progress; enforce unique team/challenge solve and derive score from accepted solves.
- **Ankit:** Test organizer role access and document account/role setup.
- **Rohit:** Verify answer-key access boundaries and solve/score behavior against rules.
- **Harsha:** Deliver reusable NPC states for briefing, clue/reaction, and solve/unlock.
- **Gate:** Progress survives refresh, is isolated by team, and duplicate solves cannot add points.

### Day 8 - Unlocks, hints, and gamified feedback
- **Akash:** Confirm unlock/hint rules; defer nonessential achievements.
- **Jagath:** Implement room unlock/progress UI, hint feedback, and NPC/story updates after solves.
- **Bhavya:** Test locked direct URLs, unlock conditions, hint states, keyboard feedback, and reduced motion.
- **Kushal:** Verify configured unlock, points, hints, and evidence against source material.
- **Aryamaan:** Verify NPC dialogue and reveal sequence against existing story.
- **Jashwanth:** Enforce unlocks and hint policy server-side on every protected request.
- **Ankit:** Test organizer pause/disable flow and draft participant notice.
- **Rohit:** Compare implemented score/hint/progression behavior with published rules; log mismatches.
- **Harsha:** Review the loop objective -> action -> feedback -> progress -> next objective; refine NPC states.
- **Gate:** Team completes one room and sees correct score, progress, unlock, and story feedback.

### Day 9 - Scoreboard and organizer-console slice
- **Akash:** Approve scoreboard visibility, tie-break policy, and minimum admin permissions.
- **Jagath:** Implement player score/progress summary and organizer-console layout using site patterns.
- **Bhavya:** Test totals, ties, empty state, long names, role access, and paused challenge state.
- **Kushal:** Audit imported points and evidence availability across rooms.
- **Aryamaan:** Ensure incident/story status does not reveal unreached narrative.
- **Jashwanth:** Implement score query and permission-gated organizer operations for team/progress/challenge status.
- **Ankit:** Exercise find-team, inspect-progress, pause-challenge, and record-score-issue scenarios.
- **Rohit:** Verify tie-break/rules and score calculation using the source answer/point map.
- **Harsha:** Review visual distinction between score, completion, and story progress.
- **Gate:** Score derives from accepted solves; organizer actions are permission-gated.

### Day 10 - Integrate Rooms 1-5; midpoint review
- **Akash:** Lead P0 midpoint review; cut or defer features if behind.
- **Jagath:** Integrate frontend content for Rooms 1-5.
- **Bhavya:** Run Rooms 1-5 acceptance tests with a clean team and log reproducible defects.
- **Kushal:** Verify Rooms 1-5 staging assets/metadata against manifest/checksums.
- **Aryamaan:** Verify Rooms 1-5 story, NPC triggers, and transitions in staging.
- **Jashwanth:** Verify Rooms 1-5 API/answer records and inspect public responses for secret leakage.
- **Ankit:** Test rules/help links and admin visibility across Rooms 1-5.
- **Rohit:** Independently solve Rooms 1-5 through the platform; report mapping/verification failures only.
- **Harsha:** Review Rooms 1-5 in the running build; address high-impact NPC/design issues.
- **Gate:** Rooms 1-5 are playable end-to-end and the schedule remains feasible.

### Day 11 - Integrate Rooms 6-10
- **Akash:** Review the full map and prevent new features entering the sprint.
- **Jagath:** Integrate frontend content for Rooms 6-10 and completion state.
- **Bhavya:** Run Rooms 6-10 acceptance tests with a fresh team.
- **Kushal:** Verify Rooms 6-10 assets, metadata, checksums, links, and fallbacks.
- **Aryamaan:** Verify Rooms 6-10 story transitions and ending in the build.
- **Jashwanth:** Verify server-side records, unlocks, team scope, and final-room access.
- **Ankit:** Exercise organizer scenarios against the ten-room build.
- **Rohit:** Independently solve Rooms 6-10 and verify answers/points against rules.
- **Harsha:** Review NPC presence and visual consistency through the final reveal.
- **Gate:** Full ten-room route is playable; any failing task is disabled or has an owned fix.

### Day 12 - Content integrity and full-flow integration
- **Akash:** Approve challenge disable/cut decisions and protect the release date.
- **Jagath:** Fix cross-room navigation, direct links, responsive layout, and display defects.
- **Bhavya:** Run full journey from sign-in to final room, including refresh and re-entry.
- **Kushal:** Reconcile every challenge record and evidence file against source.
- **Aryamaan:** Reconcile all story text, NPC triggers, and reveal order against source.
- **Jashwanth:** Verify every active ID has server-side validation/points; inactive IDs cannot score.
- **Ankit:** Verify rules, help, announcements, and admin controls throughout the experience.
- **Rohit:** Reconcile all answer keys and independently verify at least one solve per room.
- **Harsha:** Sign off NPC assets, fallback, legibility, and desktop/mobile fit.
- **Gate:** No active placeholder or broken reference; source differences are approved.

### Day 13 - Organizer workflow complete
- **Akash:** Review P0 status and defer P1 features that threaten testing.
- **Jagath:** Complete organizer UI states and role-based navigation/feedback.
- **Bhavya:** Test invalid admin actions, challenge pause/re-enable, team lookup, and audit visibility.
- **Kushal:** Back up organizer-only source package and evidence fallback with restricted access.
- **Aryamaan:** Ensure final story/NPC content appears only at the correct progression state.
- **Jashwanth:** Secure admin APIs and log consequential actions where supported.
- **Ankit:** Run organizer workflows with least-privilege access; confirm escalation and participant messaging.
- **Rohit:** Finalize runbook for access, support, answer-key custody, outages, score disputes, and escalation.
- **Harsha:** Review full gamified experience for clarity; finish only P0 design/assets.
- **Gate:** Organizers can run the platform without developer-only access or undocumented steps.

### Day 14 - Security, accessibility, and browser pass
- **Akash:** Review risks and approve only launch-critical fixes.
- **Jagath:** Fix keyboard access, focus, responsive states, accessible labels, and reduced-motion behavior.
- **Bhavya:** Test cross-team, locked-room, duplicate-submit, malformed-input, permissions, and browser cases.
- **Kushal:** Check asset safety, privacy, provenance, checksums, downloads, and restricted access.
- **Aryamaan:** Ensure internal story/answer notes are not rendered to players and framing stays fictional.
- **Jashwanth:** Verify authorization, server-side answers, rate limits, stack-appropriate CSRF/XSS protection, secrets, backups, and rollback.
- **Ankit:** Test admin workflows and incident notices using organizer access.
- **Rohit:** Audit rules, answer-key handling, hints, and score behavior against implementation.
- **Harsha:** Check NPC contrast/legibility and provide accessible fallback treatment.
- **Gate:** No known critical security, privacy, accessibility, score, or operations defect.

### Day 15 - Feature freeze and release candidate
- **Akash:** Freeze P0 scope; record open defects, release owner, and go/no-go thresholds.
- **Jagath:** Prepare frontend release candidate and verify all player routes.
- **Bhavya:** Run acceptance suite and publish pass/fail evidence.
- **Kushal:** Lock import manifest and archive checksums/source files.
- **Aryamaan:** Lock approved story/NPC trigger map; allow only defect fixes afterward.
- **Jashwanth:** Prepare backend release candidate and deployment/rollback checklist.
- **Ankit:** Freeze organizer permissions and verify runbook steps.
- **Rohit:** Sign off rules, player journey, answer mappings, and key custody against release candidate.
- **Harsha:** Sign off core NPC assets and game visual states.
- **Gate:** Release candidate exists; P1 work stops unless all P0 tests pass.

### Day 16 - Independent playtest
- **Akash:** Recruit testers unfamiliar with the platform and set up test teams/window.
- **Jagath:** Prepare stable playtest build and resettable test accounts.
- **Bhavya:** Observe without coaching and maintain severity-ranked reproducible issues.
- **Kushal:** Triage import/evidence issues and verify downloads on tester devices.
- **Aryamaan:** Observe story/NPC comprehension and report source mismatches.
- **Jashwanth:** Monitor backend errors without exposing secrets; diagnose failures.
- **Ankit:** Run participant rules/support and organizer-admin simulations.
- **Rohit:** Observe solve/submission behavior and identify rule/runbook gaps.
- **Harsha:** Observe NPC/game visual comprehension and whether cues support the next action.
- **Gate:** Playtest complete; critical/high issues have owners, fix plans, and retests.

### Day 17 - Fix and retest
- **Akash:** Prioritize defects and reject scope expansion.
- **Jagath:** Fix high-severity frontend/navigation defects and retest changed routes.
- **Bhavya:** Retest closed issues and rerun core acceptance/security checks.
- **Kushal:** Retest affected imports/assets and refresh release manifest.
- **Aryamaan:** Retest story/NPC trigger sequence after integration fixes.
- **Jashwanth:** Fix high-severity backend/security defects; verify persistence/recovery.
- **Ankit:** Retest runbook against corrected build and resolve procedure mismatches.
- **Rohit:** Reverify impacted answers, points, rules, and solve paths; keep keys private.
- **Harsha:** Retest changed art/layout and NPC rendering at target sizes.
- **Gate:** No open critical/high defect without Akash's documented acceptance and workaround.

### Day 18 - Reliability and deployment rehearsal
- **Akash:** Lead go/no-go rehearsal and confirm release authority.
- **Jagath:** Test site entry, navigation, refresh, mobile, and fallback route.
- **Bhavya:** Run multi-team concurrency/score smoke checks and retain evidence.
- **Kushal:** Simulate broken evidence and validate organizer fallback.
- **Aryamaan:** Verify complete room/story sequence on release candidate.
- **Jashwanth:** Rehearse deploy, backup, rollback, monitoring, and escalation in staging.
- **Ankit:** Rehearse announcements, participant support, challenge pause, score dispute, and close-out.
- **Rohit:** Run independent solve-through and validate official score/tie rules.
- **Harsha:** Check NPC loading on desktop/mobile and graceful fallback.
- **Gate:** Deployment and operations rehearsed; no feature work remains.

### Day 19 - Production deployment and smoke test
- **Akash:** Approve deployment window and notify stakeholders.
- **Jagath:** Verify production integration, routes, and player UI after deployment.
- **Bhavya:** Run production smoke tests with test teams; stop release on P0 failure.
- **Kushal:** Verify production evidence access, checksums, and organizer backups.
- **Aryamaan:** Verify production story/NPC sequence and no premature reveal.
- **Jashwanth:** Deploy; verify health, logs, permissions, backups, and rollback access.
- **Ankit:** Verify organizer access, support channel, runbook, and announcements.
- **Rohit:** Verify representative answers, score rules, and key custody in production.
- **Harsha:** Check NPC/game visuals across target viewports.
- **Gate:** Production smoke passes; otherwise roll back or disable affected feature.

### Day 20 - Go/no-go and event readiness
- **Akash:** Record launch decision against release gates and communicate it.
- **Jagath:** Confirm event link, player entry, room map, and challenge routes.
- **Bhavya:** Run final smoke: team entry -> room -> challenge -> submit -> score -> unlock.
- **Kushal:** Confirm imported content/assets, checksums, and fallbacks are available to organizers.
- **Aryamaan:** Confirm story/NPC sequence and final reveal are ready.
- **Jashwanth:** Confirm deployment health, monitoring, backup/rollback access, and on-call handoff.
- **Ankit:** Open runbook; coordinate support, announcements, organizer actions, and close-out.
- **Rohit:** Confirm rules, private-key custody, challenge verification, and score-dispute procedure.
- **Harsha:** Confirm NPC assets are loaded and accessible; report only release blockers.
- **Gate:** Go/no-go recorded; all owners know their event role and escalation path.

## Release Gates

- **Day 6 - Vertical slice:** A test team enters, opens one real room/challenge, accesses evidence if applicable, submits an answer, receives a server-validated result, earns points once, and sees progress. No private answer is in client data.
- **Day 12 - Feature complete:** Ten rooms and existing challenge content are integrated; team isolation, unlocks, hints, score, NPC/story feedback, and minimum organizer workflow work in staging.
- **Day 15 - Release candidate:** Feature freeze; acceptance suite passes; answer mappings/assets are verified; deployment and rollback are documented.
- **Day 20 - Launch:** Production smoke test passes, no unresolved critical defect, rollback is available, and organizers/runbook/support are ready.

## Risk and Scope Controls

1. **Unknown existing stack or access:** Resolve on Day 1. If blocked, Akash escalates immediately; do not start a parallel platform.
2. **Incomplete challenge package:** Kushal tracks missing records/assets; Rohit verifies mappings. Only verified challenges are enabled; no new challenge authoring is in this scope.
3. **Frontend/backend drift:** Jagath and Jashwanth agree contracts on Day 2 and prove them in the Day-6 vertical slice.
4. **Gamification scope growth:** P0 is progress, score, unlocks, feedback, and NPC/story beats. Badges, branching endings, realtime systems, and custom labs are P1.
5. **NPC asset delay:** Harsha supplies a minimum usable NPC asset/state early; the UI has a fallback so art cannot block gameplay.
6. **Late defects:** After Day 15, only security, data-integrity, broken-flow, imported-content solvability, or availability fixes are allowed. Akash records accepted risks.

## Source Documents

- Story and existing challenges: [Proposed_Story_Plan - 1.md](Proposed_Story_Plan%20-%201.md)
- Solve-location and platform architecture notes: [ChatGPT_Plan_Cybersecurity_Escape_Room.md](ChatGPT_Plan_Cybersecurity_Escape_Room.md)
