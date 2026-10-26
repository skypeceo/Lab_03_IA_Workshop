# Expectation for one additional candidate

The five base results are supplied. This expectation concerns YOUR additional run.

- Base model: `tree` (DecisionTreeClassifier, `min_samples_leaf=50`, `class_weight='balanced'`, seed 414).
- Parameter and old → new value (one allowed tuple): `max_depth` 3 → 6.
- Conditions held fixed: same CSV (hash checked by `load_learning`), train 2018–2021 / dev 2022 rounds 1–11,
  the nine `FEATURES`, the same preprocessing fitted on train only, seed 414, every other tree parameter,
  and the same threshold policy on dev (≤10% alerts = ≤945 windows, maximise distinct entries detected,
  then precision and threshold as tie-breakers). The threshold is re-selected for the candidate, so its
  numeric value may differ from the parent's 0.714.
- Have you already run this additional candidate? **No.** This expectation was written before the first run
  (Mon 26 Oct 2026), after inspecting only the supplied base outputs.
- Expected effect and mechanism, written before the first additional run:
  The parent tree has only 8 leaves, so on dev it gives 8 distinct scores. The policy stops at 571 alerts (6.0%),
  because the next tied leaf would add enough windows to reach 1898 alerts, over the 945 limit. That leaves 4% of
  the budget unused. A depth-6 tree can have up to 64 leaves: its scores are finer, so we expect the selected
  threshold to use more of the budget (closer to 945 alerts) and the number of distinct entries detected to rise
  above the parent's 63/370 (0.170).
  We do not expect it to beat `forest_sqrt` (140/370), because a single tree does not average away noise.
  We also expect a larger train/dev gap than the parent: deeper splits with leaves of ≥50 rows can fit
  circuit/compound combinations specific to 2018–2021. Precision may move either way; with more alerts we expect
  it to stay near the parent's 0.270 or drop slightly.
- Other trials already made, if any, and how the final candidate was chosen: none. We chose this tuple by
  reasoning from the base table (the parent tree's unused budget) and did not run the other two tuples.

Keep this record after running, even if wrong. Explain actual results in “4. Explain your additional result”.
Do not rewrite an expectation as if it predicted a result already seen.
