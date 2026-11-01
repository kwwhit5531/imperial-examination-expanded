# Imperial Examination Expanded: vanilla investigation

Inspected installed files on 2026-10-31. No mod scripts or base-game edits have been made. This report completes the requested investigation stage; implementation and in-game validation remain future work.

## Installed target

- Installation: `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/`.
- `launcher/launcher-settings.json`: version **1.20.1.2 (Crozier)**, rawVersion `1.20.1.2`.
- Steam appmanifest: build **26046173**.
- `game/dlc/dlc022_ep4/dlc022.dlc` identifies **All Under Heaven**. Presence of the DLC files does not establish that it is enabled in a running game.

All source references below are relative to the installation's `game/` folder. Line numbers refer to this installed build.

## Activity architecture and event selection

| Context | Definition and dispatch | Event selection |
| --- | --- | --- |
| Local / provincial activity | `common/activities/activity_types/local_examination.txt`, phases start at 1026 | Assembly and preparation call `imperial_examination_pulse` weekly (1053, 1075). Examination calls `imperial_examination_exam_entrant_events` weekly for entrants with `local_exam_taker_intent` (1135–1148). |
| Capital / metropolitan activity | `common/activities/activity_types/imperial_examination.txt`, phases start at 758 | Same assembly/preparation pulse (785, 807); same entrant examination pool for `imperial_exam_taker_intent` (865–877). |
| Palace examination | A later phase of the imperial activity, starting at 952 | Calls the shared entrant examination pool once on phase activation for `palace_entrants` (998–1009). Separate palace preparation pool is scheduled after 9, 17, and 24 days (1011–1023); weekly pulse is empty (1032). |

Local and metropolitan activities have assembly, preparation, and examination phases. Assembly uses a 15-day script value; preparation uses 30 days. Both examination phases explicitly schedule progression after **six weeks**, even though an `imperial_examination_exam_days = 30` script value also exists. Use the actual phase callbacks when reasoning about event opportunities.

`common/on_action/activities/imperial_examination_on_actions.txt` contains:

- `imperial_examination_pulse`: chooses between assembly and preparation child on-actions, each weight 1; their triggers enforce the appropriate activity type and phase.
- `imperial_examination_assembly_events`: shared role-dependent assembly pool.
- `imperial_examination_prep_events`: shared preparation pool.
- `imperial_examination_exam_entrant_events`: nine equally weighted entries (100 each): `.5000`, `.5050`, `.5100`, `.5150`, `.5160`, `.5170`, `.5200`, `.5300`, `.5400`. Individual triggers select the appropriate questions for phase and focus. These are not nine interchangeable generic encounters.
- `imperial_examination_exam_host_events`: three host events, but its trigger explicitly requires the imperial activity. The local activity calls this on-action too; that does not make those host events eligible locally.
- `palace_examination_prep_events`: a separate palace pool, including host and candidate narratives.

The main scripts are `events/activities/imperial_examination_activity/imperial_examination_events.txt`, `imperial_examination_events_jay.txt`, `az_examination_events.txt`, and `emperor_prep_phase_imperial_examination_events.txt` in that same directory. Existing English localization lives in `localization/english/dlc/tgp/` and activity localization in `localization/english/activities/`.

## Event scopes and eligibility

Vanilla uses `type = activity_event` and `theme = imperial_examination`. ROOT is the character receiving the event; `scope:activity` is the activity, and `scope:host` is supplied by the activity callbacks. `involved_activity` links a character back to their current activity.

Relevant guest subsets are `entrants`, `imperial_examiners`, `guests`, `failees`, `scoreboard`, and, in the palace phase, `palace_entrants`.

For each prototype event, require a valid activity scope, the local activity type, the active examination phase, entrant membership, the local exam-taker intent, and continued participation at the activity location. Require a living valid second character before selecting an encounter that needs one. A trigger must establish availability before immediate effects choose and save a portrait character.

The vanilla helper `imperial_examination_fetch_other_entrant_effect` (main event file, 357) excludes ROOT and checks `involved_activity ?= scope:activity`: vanilla explicitly warns that attendance lists can retain departed characters. Apply the same check when selecting mod characters, with alive/location checks where relevant.

`imperial_examination_fetch_examiner_effect` (321) selects an AI examiner, but creates and adds one if none exists. Prefer requiring an existing eligible examiner for mod encounters rather than introducing new people just to make an event possible.

These helpers, the advantage setup, and the score helper are declared with inline `scripted_effect` in the vanilla event file. Do not assume those file-local definitions are callable from a separate mod event file. Define uniquely named reusable mod helpers under `common/scripted_effects/`, using the verified primitive operations, rather than depending on their visibility.

## Performance and passing

There is no single universal Learning-to-pass percentage.

- `common/script_values/tgp_imperial_examination_values.txt`: `imperial_examination_entry_value` begins at 272 and incorporates skills and other bonuses; Learning and education are among the inputs.
- The main event file's `imperial_examination_exam_duel_effect` uses a skill duel with Learning, Martial, and Stewardship, then modifies outcome weights for activity focus, advantages, Confucian education, and other conditions. For local examinations, Learning and Stewardship explicitly contribute to a success weight. Different questions can have additional mechanics.
- `imperial_examination_add_score_effect` (5522) updates **both** `temporary_exam_score` and `imperial_examination_score`, initializing either if absent. The former feeds phase elimination; the latter feeds the scoreboard, rewards, and other checks.
- Actual script values: ordinary success **10**, great success **20**, critical success **40**, cheat outcome **30**. `num_intermediate_exams_value = 3`. Some nearby comments contain older numbers; use executable values rather than those comments.
- `imperial_examination_determine_exam_outcome_effect` (scripted effects file, 1692) marks caught cheaters and low phase scorers for failure using the activity's quota. The quota depends on AI entrant count and grade options (values file, 958).
- `imperial_examination_prune_failees_effect` (1770) explicitly exempts players from its AI pruning. Metropolitan examination also has a separate player cumulative-score check below **50** (`imperial_examination.txt`, around 897). Do not treat the general AI quota as the player's pass formula.
- Palace has its own score/ranking handling and subset changes. Its effects must be reviewed separately before enabling mod performance rewards there.

Do not change `num_intermediate_exams_value` or set vanilla question-completion variables for the new narratives: they supplement the examinations, rather than adding formal scored papers. Use a mod score wrapper that mirrors the two-variable update only in supported phases. Small adjustments, provisionally 1–3 points, are appropriate to test; 10–40 points would rival an entire vanilla question. A narrative need not award score if stress, opinion, or a small cost gives it a meaningful consequence.

## Recommended additive integration

Use a uniquely named file under `common/on_action/` that adds a mod-owned child through the existing `imperial_examination_exam_entrant_events` on-action's `on_actions` list. The child owns its eligibility trigger and `random_events` pool. Do not replace the vanilla activity definition or its `random_events` block.

Vanilla demonstrates child `on_actions` dispatch and `chance_of_no_event` in `common/on_action/activities/pilgrimage_on_actions.txt`. The exact merge behavior of our supplemental definition, inherited activity scopes, and coexistence with vanilla random event dispatch must be confirmed in the prototype. Static source inspection is not an engine test.

This approach can produce a supplementary narrative alongside a vanilla question on the same weekly pulse. It deliberately keeps the formal question pool intact. Start with an approximately 15–20% chance per eligible weekly pulse and a per-character narrative spacing guard, then measure actual frequency. Lower relative event weights alone would not limit the total firing rate of an independent supplementary pool. Adding all 15 entries directly to the nine-entry question pool risks delaying the formal papers and is not recommended.

Put tier and phase rules in a shared mod trigger, character selection and score changes in mod helpers, and all narratives in one shared event set. For the prototype, only the local examination phase passes the tier trigger. Every event should also enforce its own eligibility so a misrouted dispatch cannot make it appear outside an examination.

For capital/metropolitan support, broaden that trigger to the imperial examination phase and imperial exam-taker intent. The dispatch already reaches the same shared on-action, so event duplication is unnecessary. Gate classical-only content against a martial focus when its premise requires a written classical paper.

Palace support needs more than adding an activity type: recognize `palace_entrants`, account for the one-time entrant dispatch rather than a weekly loop, and verify palace score effects. Use the palace preparation hook only for narratives appropriate to that phase. No independent additional examination activity type was identified in the two activity definitions inspected; child or other examination systems must receive their own investigation before being declared compatible.

## Variety and repetition

Vanilla narrative events frequently use `cooldown = { months = 6 }`; formal questions instead use variables such as `had_essay_examination`, `had_classics_examination`, and `had_poetry_examination`. Vanilla phase cleanup removes those question markers and selected vanilla narrative/advantage variables (`tgp_imperial_examination_scripted_effects.txt`, 1793).

Use both a modest event cooldown (initially 12 months) and explicit per-character/per-activity seen state for each mod event. Store or compare the activity reference so an event cannot repeat for the same candidate during that examination, and a subsequent activity can become eligible without overriding vanilla cleanup. A short shared spacing guard should limit clustering across different mod events. Verify activity-reference expiry behavior in game. For strict activity-wide uniqueness across all attendees, activity-owned state would be required; per-character guards alone do not promise that.

Use `weight_multiplier` (demonstrated in the main vanilla event file around 2057) for personality/context variation and conditional availability for rivals or familiar faces. Keep a normal fallback pool so special relationship requirements do not starve selection.

## Prototype and validation gate

Recommended first three: difficult passage, suspected cheating, and a flawed question. Together they exercise candidate selection, examiner selection, Learning-sensitive outcomes, personality choices, and small performance changes. Write at least three choices apiece with generic tier-neutral text.

Before the remaining twelve are implemented:

1. Load only the prototype and All Under Heaven in a debug-enabled game; confirm installed version and active DLC.
2. Attend a real local examination as an entrant and observe the natural weekly dispatch. Console-forcing an event is useful for option checks but does not prove integration.
3. Verify every option and success/failure branch; inspect both score variables, stress/opinion/cost changes, AI choice behavior, localization, and portraits.
4. Exercise missing-examiner, no-second-candidate, departed/dead-character, and interrupted-activity cases. Events requiring those characters must become ineligible.
5. Confirm no natural triggers during travel, preparation, unrelated activities, or capital/palace examinations while local-only mode is enabled.
6. Observe a complete examination for repeats and clustering; attend another to check activity-scoped markers and timed cooldowns. Compare vanilla question completion and final results against an unmodded run.
7. Check the resolved user-data `logs/error.log` and relevant debug logs for parser, missing localization, invalid effect, and invalid scope errors. Record save/setup, event IDs, observed outcomes, and log excerpts.

No game session, option execution, merge test, or log validation has yet occurred. Source inspection establishes an implementation plan, not a tested prototype.

## Implementation-stage addendum

The subsequent prototype investigation also read `common/on_action/_on_actions.info`: lines 106–119 explicitly document extending a vanilla on-action through a separate `on_actions` child definition. Lines 56 onward document `chance_to_happen` as a percentage gate and event weights as relative selection weights. The prototype uses that documented additive pattern and a 20% gate. Runtime status is tracked separately in `TESTING.md`; the original investigation-stage status above describes the earlier checkpoint.
