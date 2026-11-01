# Imperial Examination Expanded

## Overview

The working source now contains **15 events**: nine candidate events and six events for the **Assist Examination** intent. See [the event catalogue](EVENT_PLAN.md) for the twelve additions. Candidate events occur during the active local examination; assistance events occur during local assembly/preparation. Both roles use 14-day spacing and per-event repetition guards. The new assistance pool has a 35% weekly chance; the candidate pool retains 20%.

The expanded structural validator passes (15 events, 87 localization keys). Runtime testing of the expansion is pending. The prototype ZIP and the historical results below describe the original three-event build, not this expanded source. Restart CK3 to load changed scripts; use the isolated profile for testing.

Development expansion for Crusader Kings III **1.20.1.2 (Crozier)** with **All Under Heaven**. English localization is included for all 15 events.

[Download the older three-event prototype ZIP](packages/Imperial_Examination_Expanded_Prototype_0.1.0.zip). **This packaged ZIP does not include the twelve new events.** To get all 15, download the current repository using **Code → Download ZIP**, extract it, and install the mod folder and `.mod` file as described below. Full gameplay validation is still pending; see [testing status](TESTING.md).

The expansion supports **local examinations**. Capital and palace examinations are currently ineligible. The panel title may include the activity prefix, for example **Local Examination: A Passage Between Us**.

## Candidate events

These nine encounters require attendance as a candidate during the **active examination phase**. The first three are the original prototype encounters.

| ID | Encounter | Choices and consequences |
| --- | --- | --- |
| `iee_examination.0001` | A Passage Between Us | Explain a difficult passage with a Learning check (+2 performance on success, +5 stress on failure); admit uncertainty and listen (+5 opinion, +5 stress); rest instead (−5 stress). Personality adds stress or relief. |
| `iee_examination.0002` | A Fold of Paper | Discreetly ask an examiner to check (+5 examiner opinion, +5 stress); inspect before accusing (Learning check for candidate gratitude and relief, or suspicion and stress); concentrate on your own work (−5 stress, with personality consequences). Suspicion never automatically disqualifies anyone. |
| `iee_examination.0003` | A Word Out of Place | Respectfully challenge an apparent error (Learning check: +2 performance and examiner approval, or −1 performance and +5 stress); address both readings (+2 performance, +10 stress); skip the disputed point (−1 performance, −5 stress). |
| `iee_examination.0004` | The Rain Between the Lines | Rain blots your answer. Copy the page, mark the damaged line, or trust the reader to see past the stain. |
| `iee_examination.0005` | A Name I Must Not Write | A quotation conflicts with a family naming taboo. Rephrase it, explain the family substitution, or retain the conventional wording. |
| `iee_examination.0006` | The Last Blank Space | Your argument is complete, but paper remains. Add a counterexample, clarify the conclusion, or stop writing. |
| `iee_examination.0007` | The Borrowed Cadence | Your answer sounds like your old teacher. Find your own voice, acknowledge your intellectual school, or accept its influence. |
| `iee_examination.0008` | A Bell Beyond the Wall | A funeral bell interrupts your concentration. Let the memory inform your answer, pause in observance, or steady your breathing. |
| `iee_examination.0009` | An Answer Without Ornament | Your advice on addressing villagers is too scholarly for its audience. Rewrite plainly, add a practical example, or keep the formal style. |

All numbers above are base effects. Trait-dependent stress effects and outcome probabilities are visible in game. Performance adjustments change both vanilla phase and cumulative scores. They do not grant skill increases or complete vanilla exam papers.

The six new candidate events have fixed outcomes involving stress, prestige, or piety, with some personality adjustments. They do not change examination scores or roll Learning checks.

## Assist Examination events

These six encounters require the **Assist Examination** intent, physical presence, and no registration as a candidate. They occur during **assembly and preparation**, before the actual examination phase. A character who previously passed can encounter them when attending as an assistant; passing alone does not activate these events.

| ID | Encounter | Situation and choices |
| --- | --- | --- |
| `iee_examination.0010` | Two Doors, One Queue | Arrivals block a narrow doorway. Create a separate passage, manage the queue yourself, or let attendants clear the obstruction. |
| `iee_examination.0011` | The Measure of a Candle | Uneven candles threaten unequal lighting. Redistribute them, purchase reserves, or arrange rotation. |
| `iee_examination.0012` | Names That Sound Alike | Two candidates answer to similar-sounding names. Check written identities, display names at assigned places, or request another registration check. |
| `iee_examination.0013` | The Courtyard Echo | A passage carries whispered instructions between desks. Rearrange seating, buy sound-damping mats, or give instructions before seating. |
| `iee_examination.0014` | A Place for Every Bundle | Similar travel bundles risk getting mixed up. Record numbered storage places, buy tags, or have owners identify their places. |
| `iee_examination.0015` | The Empty Water Jar | Water deliveries could interrupt the examination. Plan a route, buy extra jars, or arrange staggered refills beforehand. |

Assistant choices have fixed stress, prestige, and occasional gold consequences. Paid supply options cost **5 gold** and appear only when affordable. They never adjust candidate scores. Practical improvements are narrated outcomes, not persistent changes to the activity's furniture, supplies, or guest records.

## Installation

1. Copy **both** `imperial_examination_expanded.mod` and the `imperial_examination_expanded` folder into your CK3 user-data `mod` directory (normally `Documents/Paradox Interactive/Crusader Kings III/mod`). Create the directory if necessary.
2. Add **Imperial Examination Expanded — Prototype** to a launcher playset and enable All Under Heaven.
3. Use a new/disposable save for testing. Attend a local examination as a **candidate** to see candidate events, or select **Assist Examination** to see assistance events during assembly/preparation.
4. Restart CK3 after updating scripts so the new event definitions are loaded.

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

The candidate pool has a **20% chance per eligible weekly pulse** during the active examination. The assistant pool has a **35% chance per eligible weekly pulse** during assembly/preparation. Eligible events have equal base weights, with modest context-based bonuses for the original three encounters. A shared **14-day spacing rule** prevents consecutive weekly mod encounters. Each event also has a **12-month cooldown** and remembers the activity in which that recipient saw it.

These guards are per recipient, not a global ban on multiple characters seeing the same story. Chance is not a guarantee: a full examination can contain no mod event. The mod pools supplement vanilla encounters and may appear on the same pulse as a vanilla event. They do not replace or dilute the formal-paper pool.

## Structure and expansion

- `common/on_action/iee_examination_on_actions.txt`: additive hook and frequency.
- `common/scripted_triggers/iee_examination_triggers.txt`: local tier/phase eligibility and character validity.
- `common/scripted_effects/iee_examination_effects.txt`: scoped selection, seen markers, and guarded dual-score updates.
- `events/iee_examination_events.txt`: shared narrative definitions.
- `common/opinion_modifiers/iee_examination_opinions.txt`: small decaying opinions.
- `localization/english/iee_examination_l_english.yml`: English text, encoded with UTF-8 BOM like the scripts.
- `tests/iee_examination_tests.txt`: an opt-in CK3 engine test for outside-activity rejection.

To enable the metropolitan phase later, broaden `iee_is_exam_candidate_trigger` to pair the imperial type/phase with its intent, without duplicating events. Palace support additionally needs `palace_entrants`, phase-specific cadence, and score validation. Classical premises also need focus checks before being offered in martial examinations.

See [VANILLA_EXAMINATION_FINDINGS.md](VANILLA_EXAMINATION_FINDINGS.md) for the original source investigation, [TESTING.md](TESTING.md) for the runtime checklist and recorded results, and [EVENT_PLAN.md](EVENT_PLAN.md) for the twelve implemented additions. The event scripts include plain-language comments explaining eligibility, choices, effects, and random outcomes. Structural validation passes for all 15 events; the expansion's in-game validation remains pending.
