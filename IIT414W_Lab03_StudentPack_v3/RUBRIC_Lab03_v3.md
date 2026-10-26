# Lab 3 rubric

100 points. Grade the evidence and explanation, including a technically justified negative result. Correctly running supplied code is necessary evidence but does not demonstrate independent design or understanding by itself. Retain the same 25/35/15/15/10 weights.

| Criterion | Components | Strong evidence | Partial evidence | Limited evidence |
|---|---|---|---|---|
| C1 Valid and controlled comparison /25 | Prediction timing and permitted inputs 7; unchanged controls and one allowed candidate 8; policy and window/event denominators 10. | 23–25: the executed comparison is valid and the pair identifies the target, time, inputs, controls and denominators correctly. | 14–22: mainly valid comparison with a specific control, policy or denominator omission. | 0–13: leakage, altered populations, uncontrolled changes or unusable comparison. |
| C2 Technical reasoning /35 | Base comparison and mechanism 7; additional candidate versus parent with at least two actual numbers 10; three distinct supported failure patterns 12 (4 each); bounded recommendation and selection/timing limits 6. | 32–35: technically sound mechanism tied to actual results; three supported patterns; observations separated from hypotheses; defensible decision with limits. | 20–31: some actual evidence and plausible reasoning, but a mechanism, pattern, denominator or decision is incomplete. | 0–19: generic claims, unsupported patterns, contradiction with results, or claims of independence/calibration/strategy gains not established. |
| C3 Memo for its audience /15 | Understandable audience/language 5; relevant accurately translated evidence and denominators 4; coherent recommendation, limitation and next check 4; one-page scope 2. | 14–15: reader can understand the recommendation, evidence and limits without decoding ML jargon; concise and within scope. | 8–13: mostly accurate but audience, structure, evidence, next step or concision needs work. | 0–7: absent, generic, materially inaccurate or not understandable to the stated reader. |
| C4 Reproducibility and consistency /15 | Accessible final commit and sufficient environment/run instructions 6; fresh execution including the additional candidate and error exports 5; agreement of notebook, CSV, generated table and memo 4. | 14–15: submitted version can be reconstructed and checked; artefacts agree and paths are portable. | 8–13: identifiable executed evidence with a recoverable setup or limited consistency omission. | 0–7: reproduction blocked by missing essential material or materially unsupported/inconsistent numbers. |
| C5 Traceability and critical AI use /10 | Correct common audit with precise repository evidence 5; truthful use/no-use and concrete verification when AI was used 3; both contributors with actions and locations 2. | All components demonstrated. A truthful no-use record can receive all 3 use-record points. | Award demonstrated components; generic verification or an audit without a precise citation is incomplete. | Missing or false records do not earn their component points. Do not infer undisclosed use or authorship from style. |

## How to keep the criteria distinct

C1 judges whether the comparison and the explanation of its protocol are valid. C2 judges the technical account of what happened, including three failure patterns. C3 judges how that evidence is translated for the memo's reader. C4 checks whether the delivered version can actually be reproduced and whether its artefacts agree. C5 checks the stated audit, record and contributions.

A failure-pattern entry earns its four points through a distinct error/context definition (1), a correct count/denominator and traceable example (2), and a bounded consequence/next check (1). A proposed cause must be marked as a hypothesis unless measured. An FN window is not automatically a missed event. Three copies of the same pattern do not meet the requirement. If evidence is insufficient, report the checks and limitation rather than inventing a pattern; grade the demonstrated evidence.

The same error type in different contexts can count as separate patterns when each entry states its context rule, gives its own count/denominator and traceable case, and explains a consequence and next check. Three cases of the same error in the same context count as one pattern. Changing only a context name without evidence and interpretation is incomplete. You do not need three different causes, independent groups or statistical significance. Declare overlap; do not add overlapping counts as distinct errors.

Fictional examples for interpreting the requirement (these are not Rival results):

- Acceptable entry A: “For context `compound == TOY_A`, 2 of 6 alerts are false (FP/alerts), including `toy-A-4`. These alerts require checking a rival that does not enter within the horizon; next check the neighbouring windows to see whether alerts repeat around the same situation. The six-alert sample is small.”
- Acceptable entry B: “For context `compound == TOY_B`, 3 of 10 alerts are false, including `toy-B-2`. The review burden also occurs here; next inspect the recorded timing around those cases before proposing a cause.” With their separate supporting rows, A and B count as two patterns even though both are FP. Your submission must provide the actual rows behind its own claims.
- Incomplete: “TOY_A has false alerts; TOY_B has false alerts; TOY_C has false alerts.” Context names alone supply neither counts/denominators nor cases, consequences or checks. Three IDs from TOY_A under the same rule also describe one pattern.

## Calibration examples

- A correct generated table with a generic “forests are better” paragraph can support the executed-protocol parts of C1/C4; it does not satisfy C2's mechanism and interpretation components.
- A technically sound memo full of undefined ML jargon loses audience points in C3. Do not also deduct C2 solely for that communication defect.
- An honestly losing additional candidate with a valid comparison, supported errors and a clear recommendation can reach the strongest band in every criterion.
- A copied number contradicted by the notebook affects C4 consistency. Apply a further consequence in C2 or C3 only if a distinct interpretation or recommendation is materially unsupported, and explain that consequence.

Do not assign an automatic score cap merely because saved outputs are absent: examine the fresh run and the other evidence. Do not award maximum points solely for file presence. The execution flag confirms a run, not learning. A log that agrees with code demonstrates traceability, not independent authorship or individual mastery. No additional oral assessment or favourable model result is required.
