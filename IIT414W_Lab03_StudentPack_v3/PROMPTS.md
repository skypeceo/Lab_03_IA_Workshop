# Common AI recommendation audit

Respond in at most five short lines to the recommendation quoted in the brief.
Accept/reject, methodological reason, and a precise checkable cell/function/output in this repository:

**Reject.** If 2026 results are used to choose the forest setting and the alert threshold, they become selection data. A score on that same data is optimistic and is not an independent final test, whatever year training ends.
Our protocol already reuses one split for selection: thresholds are chosen on development only, in `lab03_support_v3.py`, `evaluate_scores` (line 112: `choose_threshold(dev_scores, dev, budget=BUDGET)`).
Evidence: `outputs/run_manifest_v3.json` records `"threshold_selection": "dev only; reused unchanged on train"`, and `data/manifest_lab03_v3.json` lists 2026 data under `"excluded"`.
Hence our development numbers (e.g. forest_sqrt 140/370 in `comparison_table.md`) are not final-test results either. A 2026 check would have to be run once, with the model and threshold frozen beforehand.

## Truthful use / no-use record

Tool and use, or “No AI used for this lab”:
Google Gemini helped to orientate the work and some pieces of code.

If used, one actual suggestion (quote or faithful summary):
Gemini suggested the candidate `tree` `max_depth` 3 → 6, expecting that more leaves would let the threshold use more of the 945-alert budget and catch more than 63/370 entries.

What we accepted/rejected:
We accepted the candidate and recorded the expectation before the run. The expectation turned out mostly wrong (580 alerts, 57/370 entries), and we kept it unchanged in `experiment_spec.md`, explaining the result in section 4.

Exact check performed and repository evidence:
We re-ran Restart + Run All on our own machine and confirmed that the candidate rows in `comparison_table.md` (580 alerts, 57/370) match section 4, and that the section 5 counts match the `context_query` output in the cell with CONTEXT_VALUE = 'HARD' (334 FP / 394 alerts)

One limitation relevant to this work:
We could check the numbers against the generated outputs, but the proposed causes (e.g. wet-tyre rows being rare in training) remain hypotheses that neither did not measure.

## Contributions

- Martin Olivares:
  Set up the GitHub repository and `.gitignore`, chose the candidate configuration (section 3 configuration cell) and reviewed sections 1, 2 and 4 in the notebook, plus `experiment_spec.md`.
- Benjamin Levit:
  Added the section 5 entries in the ‘Your three entries’ cell and checked them against the query cells
