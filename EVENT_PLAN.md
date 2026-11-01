# Event plan

All events use tier-neutral language. Contextual traits influence AI choices and stress; Learning checks assess interpretation rather than guaranteeing rewards. No event grants a permanent skill point. The implemented prototype covers original themes 1, 3, and 9; IDs intentionally need not follow theme order.

| Original theme | Working title | Design direction | Required supporting scope | Status |
| --- | --- | --- | --- | --- |
| 1. Help with a passage | A Passage Between Us | A permitted interval permits clarification of loyalty and remonstrance. Explain, listen, or rest. | Another active candidate | Implemented: `.0001` |
| 2. Conflicting interpretations | Two Readings, One Classic | Reconcile the scholars, defend a textual reading, or reserve judgment. | Two other active candidates | Planned |
| 3. Suspected cheating | A Fold of Paper | Distinguish suspicion from evidence. Seek discreet review, inspect, or focus on work. | Candidate and examiner | Implemented: `.0002` |
| 4. Difficult question | The Exception to the Rule | A hypothetical pits obedience against relief of suffering. Use a close reading, reason from precedent, or give a cautious answer. | Examiner | Planned |
| 5. Nervous disruption | The Trembling Brush | A candidate cannot stop muttering. Reassure them, request an attendant's help, or tolerate the distraction. | Another active candidate | Planned |
| 6. Rival undermines confidence | A Measured Insult | A rival questions your preparation during an interval. Answer with scholarship, refuse the bait, or retaliate at a social cost. | An active candidate who is an actual rival | Planned; relationship-gated |
| 7. Exchange information | A Bargain in the Interval | Exchange recollections of commentaries while conversation is permitted, explain without demanding payment, or refuse. Never casually share live answers. | Another active candidate | Planned |
| 8. Apparent favoritism | The Examiner's Smile | Familiarity may be ordinary courtesy. Seek transparent clarification, trust the procedure, or complain with reputational risk. | Candidate and examiner | Planned |
| 9. Flawed question | A Word Out of Place | Decide whether an apparent attribution error deserves a challenge. | Examiner | Implemented: `.0003` |
| 10. Filial piety | A Duty Divided | Discuss the tension between mourning obligations and public duty. Reconcile duties, defend family obligation, or acknowledge uncertainty. | Another active candidate | Planned |
| 11. Attempted bribery | A Gift Too Carefully Wrapped | Witness an ambiguous private gift. Request a witnessed inquiry, confront the giver, or withdraw. Avoid automatically establishing guilt. | Candidate and examiner | Planned |
| 12. Familiar face | An Old Acquaintance | A recognized scholar recalls an earlier encounter. Welcome them, establish distance, or reopen an old disagreement. | Active candidate with a verified existing relationship | Planned; relationship-gated |
| 13. Practical governance | Ink and Granaries | Debate whether textual knowledge can answer a shortage of grain. Ground an answer in precedent, argue practical remedies, or concede a limit. | Another active candidate | Planned |
| 14. Rumored results | Names Behind a Screen | Overhear speculation about how work is being judged. Ask about criteria, disregard the rumor, or quietly compare notes. Never reveal final results before vanilla has decided them. | Examiner or appropriate active candidate | Planned |
| 15. Exhaustion | The Fallen Brush | A candidate collapses. Summon assistance, offer immediate care, or clear space and preserve the examination's order. Avoid severe injury rewards or easy permanent stat gains. | Another living active candidate | Planned |

The first expansion pass should reuse the existing helpers and per-event activity markers. Add a two-peer availability helper for the scholarly disagreement and relationship-specific helpers for the rival and familiar-face stories. Exhaustion may need a separate eligibility check so a portrait is not selected from someone already incapacitated. Event-specific constraints should not be put into the shared tier gate.
