# Prototype validation

Target: installed CK3 1.20.1.2 (Crozier), Steam build 26046173, All Under Heaven. Test date: 2026-10-31.

## Reproducible structural check

Run `python .\tools\validate_prototype.py` from the project directory. It checks balanced script blocks; UTF-8 BOM in scripts and English localization; the three registered activity events; three choices, cooldown, eligibility and seen guards per event; matching helper parameters; localization coverage; the additive on-action link; and initialization/update branches for both score variables. This validator does not emulate CK3's parser or simulation.

## Runtime profile

Use `.\tools\prepare_local_test.ps1 -Launch`. This launches the actual game using an isolated user-data directory at `.runtime/ck3-user`. It enables only this mod and does not disable DLC. Logs are under `.runtime/ck3-user/logs`.

The installed `_on_actions.info` explicitly documents additive definitions through `on_actions` (106–119), and documents `chance_to_happen` as a percentage gate (56). These mechanisms were verified against installed documentation before implementation.

## Required playtest gate

Do not expand to the remaining twelve events or enable other tiers until these checks pass.

| Check | How to verify |
| --- | --- |
| Natural dispatch | Play an eligible candidate in a local examination. Reach the active examination phase, allow weekly pulses, and observe the supplemental narratives. Preserve a save at phase entry. A console-forced event alone does not establish this. |
| Vanilla preservation | Confirm the formal essay/classics/poetry events still occur and complete as in the unmodded baseline. A mod narrative can arrive on the same pulse as a formal question. |
| All choices | Exercise all nine choices, including both branches of each Learning duel. Confirm the expected stress, opinion direction, performance change, and readable tooltips. |
| Score bookkeeping | For scored options, compare both `temporary_exam_score` and `imperial_examination_score` before and after. Existing values must receive +2/−1; missing values must initialize safely. |
| Outside-activity rejection | Check each event's eligibility outside any activity, during travel, preparation/assembly, and an unrelated activity. Natural dispatch must not occur. |
| Tier restriction | Verify capital and palace examinations do not offer mod encounters in this prototype. |
| Missing/invalid characters | With no eligible other candidate, `.0001` and `.0002` must be ineligible. With no eligible examiner, `.0002` and `.0003` must be ineligible. Dead or departed guest-list entries must not be selected. |
| Repetition | Observe at least one full local examination. No candidate may see the same mod event twice in that activity; different mod narratives must be at least 14 days apart. |
| Later examinations | Verify an event remains on its 12-month cooldown; after that, a new activity reference must permit it again. |
| Interrupted activity | End/leave the examination before resolving a scored option if reproducible. The score helper must refuse to change examination variables when eligibility no longer holds. |
| Logs | Review parser/runtime errors and database conflicts after startup and after each playtest. Investigate any mod-linked missing scope, effect, localization, or invalid target error. |

To inspect an event manually in the debug console, use `event iee_examination.0001`, `.0002`, or `.0003` **while already in an eligible local examination with the required supporting characters**. A console command can bypass event triggers; forcing an event out of context is not a supported play flow and may have no valid activity/portraits. Do not remove the guards from the release mod to increase test frequency.

## Recorded results

- Structural validator: **PASS** — seven script/descriptor files (including the opt-in engine test), three events, 27 English localization keys.
- First actual CK3 load: mod enabled and mounted; All Under Heaven mounted; all three `iee_examination` events loaded. CK3 reported missing UTF-8 BOM markers in the five script files. Those markers were added and the validator now checks them.
- Corrected build: CK3 completed history loading, enabled the mod, and loaded all three events with a **zero-byte `error.log`**. Evidence is preserved in `validation/2026-10-31/startup_evidence.txt`; hashes of that build are in `startup_manifest.json`.
- A subsequent direct-start run includes the opt-in outside-activity test. Its file was added while CK3 was reading databases, producing a BOM warning before conversion finished. The file now has the required BOM, verified by the structural validator. This warning must be distinguished from script/scope failures in subsequent results.
- Direct-start gameplay: **PASS for world initialization only** — the isolated 1066 game opened as Qin Guan, and the vanilla opening events and activity browser were usable. No mod event was forced outside an examination.
- Engine negative test: **NOT RUN** — the debug-console shortcuts did not open the console through the available UI automation. The test is provided for execution from a working console; its existence is not evidence that it passed.
- Natural local-examination dispatch, all nine choices/duel outcomes, score changes during examinations, and repetition across examinations: **PENDING**. The fresh Qin Guan game had no ongoing activity when inspected. Startup validation does not cover these checks.
- The disposable test process was closed after evidence collection. No ordinary user playsets or saves were edited.

The full playtest gate remains unpassed until natural dispatch, every option/outcome, negative scope cases, repeated examinations, and logs have been verified. Source checks and startup success alone cannot establish those behaviors.
