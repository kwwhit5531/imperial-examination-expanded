# Imperial Examination Expanded

## Current development expansion

The working source now contains **15 events**: nine candidate events and six events for the **Assist Examination** intent. See [the event catalogue](EVENT_PLAN.md) for the twelve additions. Candidate events occur during the active local examination; assistance events occur during local assembly/preparation. Both roles use 14-day spacing and per-event repetition guards. The new assistance pool has a 35% weekly chance; the candidate pool retains 20%.

The expanded structural validator passes (15 events, 87 localization keys). Runtime testing of the expansion is pending. The prototype ZIP and the historical results below describe the original three-event build, not this expanded source. Restart CK3 to load changed scripts; use the isolated profile for testing.

Three-event prototype for Crusader Kings III **1.20.1.2 (Crozier)** with **All Under Heaven**. English localization is included. This is the first implementation milestone of a planned 15-event expansion.

[Download the installable prototype ZIP](packages/Imperial_Examination_Expanded_Prototype_0.1.0.zip). Full gameplay validation is still pending; see [testing status](TESTING.md).

The prototype adds supplemental encounters during the **active local examination phase**. Capital and palace examinations are deliberately ineligible until local validation is complete.

| ID | Encounter | Choices and consequences |
| --- | --- | --- |
| `iee_examination.0001` | A Passage Between Us | Explain a difficult passage with a Learning check (+2 performance on success, +5 stress on failure); admit uncertainty and listen (+5 opinion, +5 stress); rest instead (−5 stress). Personality adds stress or relief. |
| `iee_examination.0002` | A Fold of Paper | Discreetly ask an examiner to check (+5 examiner opinion, +5 stress); inspect before accusing (Learning check for candidate gratitude and relief, or suspicion and stress); concentrate on your own work (−5 stress, with personality consequences). Suspicion never automatically disqualifies anyone. |
| `iee_examination.0003` | A Word Out of Place | Respectfully challenge an apparent error (Learning check: +2 performance and examiner approval, or −1 performance and +5 stress); address both readings (+2 performance, +10 stress); skip the disputed point (−1 performance, −5 stress). |

All numbers above are base effects. Trait-dependent stress effects and outcome probabilities are visible in game. Performance adjustments change both vanilla phase and cumulative scores. They do not grant skill increases or complete vanilla exam papers.

## Installation

1. Copy **both** `imperial_examination_expanded.mod` and the `imperial_examination_expanded` folder into your CK3 user-data `mod` directory (normally `Documents/Paradox Interactive/Crusader Kings III/mod`). Create the directory if necessary.
2. Add **Imperial Examination Expanded — Prototype** to a launcher playset and enable All Under Heaven.
3. Use a new/disposable save for prototype testing. Enter a local examination as a **candidate**, rather than hosting or assisting it.

The folder beside the `.mod` file must contain `descriptor.mod`, `common`, `events`, and `localization`. Do not copy the repository itself into an extra nested mod folder. No base-game files need editing.

## Isolated development profile

Run from PowerShell in this project:

```powershell
python .\tools\validate_prototype.py
.\tools\prepare_local_test.ps1 -Launch
```

The second command prepares `.runtime/ck3-user`, enables the workspace mod there, and starts CK3 in debug mode with `-userdir` pointing to that profile. It leaves the normal CK3 user directory alone and refuses to launch a second CK3 process. Logs and test saves stay under `.runtime/ck3-user`. Without `-Launch`, it only prepares the profile. The install path in this helper currently targets the inspected Steam installation.

Add `-StartAsCandidate` to start a fresh 1066 game as Qin Guan using CK3's documented `-skip`, `-bookmark`, and `-play` options. Before joining an activity, the debug-console command `scripted_tests iee_outside_activity` checks the outside-activity gate and score-effect rejection. The test changes no examination scores when it passes.

## Event frequency

The vanilla entrant examination on-action calls an additional mod-owned child. The child has a **20% chance per eligible weekly pulse**, followed by an equal-weight choice between eligible encounters, with modest context-based weight bonuses. A 14-day recipient spacing flag prevents consecutive weekly mod encounters. Each event also has a 12-month cooldown and remembers the activity in which that candidate saw it.

These guards are per recipient, not a global ban on multiple candidates seeing the same story. Chance is not a guarantee: a full examination can contain no mod event. The new pool supplements vanilla's questions and may appear on the same pulse as a vanilla event. It does not replace or dilute the formal-paper pool.

## Structure and expansion

- `common/on_action/iee_examination_on_actions.txt`: additive hook and frequency.
- `common/scripted_triggers/iee_examination_triggers.txt`: local tier/phase eligibility and character validity.
- `common/scripted_effects/iee_examination_effects.txt`: scoped selection, seen markers, and guarded dual-score updates.
- `events/iee_examination_events.txt`: shared narrative definitions.
- `common/opinion_modifiers/iee_examination_opinions.txt`: small decaying opinions.
- `localization/english/iee_examination_l_english.yml`: English text, encoded with UTF-8 BOM like the scripts.
- `tests/iee_examination_tests.txt`: an opt-in CK3 engine test for outside-activity rejection.

To enable the metropolitan phase later, broaden `iee_is_exam_candidate_trigger` to pair the imperial type/phase with its intent, without duplicating events. Palace support additionally needs `palace_entrants`, phase-specific cadence, and score validation. Classical premises also need focus checks before being offered in martial examinations.

See `VANILLA_EXAMINATION_FINDINGS.md` for source evidence, `TESTING.md` for the runtime checklist and recorded results, and `EVENT_PLAN.md` for the remaining twelve concepts. The remaining events must wait until the prototype's runtime gate passes.
