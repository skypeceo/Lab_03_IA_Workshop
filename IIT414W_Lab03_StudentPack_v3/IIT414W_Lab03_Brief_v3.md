# Lab 3 Model comparison and a defensible recommendation

IIT414W · 100 points · 6% NP · same pairs as Lab 2

Due Thursday 29 October 2026 at 12:30, Santiago time. Submit one Canvas text entry per pair: both names, an instructor-accessible GitHub URL, final commit ID and notebook path.

## How this lab builds on your previous work

In Lab 1 you checked data and compared simple prediction rules. In Lab 2 you changed one input while keeping the comparison conditions fixed. In Lab 3 you keep the inputs fixed and change one model setting. You will explain the result, examine its errors and write a recommendation for a reader who does not know machine learning. You are assessed on the evidence and reasoning behind that recommendation, including when your change performs worse.

The prediction task also changes: Lab 2 used synthetic pre-race top-10 data; this lab reuses the real Rival Pit Window case from 16 October. At the end of a rival driver's lap L, predict whether that driver will enter the pits during their own next three laps. This is an observed entry, not an optimal pit-stop recommendation for your own car.

The supplied code handles loading, preparation, fitting, threshold selection and exports. Your contribution is to check the protocol, specify one change, interpret actual results, identify three supported failure patterns and communicate a bounded decision. Running the unchanged starter does not complete the lab.

## Start here and follow this order

Download and extract the complete ZIP. Open `README.md` for the environment check, then `Lab03_ModelComparison_Student_v3.ipynb`. All steps below have a matching notebook heading; do not create extra reports.

| Step | What you do | Where your work belongs | Ready when |
|---|---|---|---|
| 1 Check the prediction | Explain target, prediction time, one allowed input and one future-known field kept out of X. | “1. Define the prediction” | Your answer refers to this dataset and its timing limits. |
| 2 Read the base comparison | Reproduce two references and three learned models; interpret their development results and one train/dev gap. | “2. Explain the common comparison” | You distinguish windows, events, alerts and the two populations. |
| 3 Specify one change | Record the parameter, old/new values, fixed conditions and expectation before the additional run. | `experiment_spec.md` | The expectation concerns the new candidate, not the already supplied base outputs. |
| 4 Run and explain | Set the three fields in “3. Record your expectation before your additional run” (configuration block), run that configuration and compare with the unchanged parent. | “4. Explain your additional result” | At least two observed numbers support an explanation of the change. |
| 5 Examine errors | Identify three distinct failure patterns in your candidate's development predictions, using the supplied context tables and cases. | “5. Explain three distinct failure patterns” → “Your three entries” | Each pattern has a count/denominator, example ID, consequence and next check. |
| 6 Recommend and submit | Write a one-page memo, complete the common AI audit and truthful record, then restart and run all. | `memo.md`, `PROMPTS.md` and executed notebook | Six systems produce twelve train/dev rows; outputs agree and the final commit is accessible. |

## Conditions that stay fixed

- Train: 2018–2021. Development: first eleven rounds of 2022. Keep the included CSV unchanged, seed 414 and the nine permitted inputs in `FEATURES`. Preparation and models fit on train only.
- Five base systems: `never_alert`, `historical_baseline`, `tree`, `forest_all`, `forest_sqrt`. The two forests differ only in `max_features`. No additional model family, feature search or random split.
- Choose one additional change: `tree: max_depth 3 → 6`; `forest_sqrt: max_depth 6 → 3`; or `forest_sqrt: min_samples_leaf 30 → 100`. Do not try all three and silently report only the best. Disclose any additional trials already made.
- Do not use remaining 2022 races, 2023–2024 test data or 2026 results to choose models, features or thresholds. These files are excluded from the ZIP. No SHAP, calibration study, new data collection or paid tool is required.

Choose one additional configuration. You may rerun that same configuration for debugging and Restart + Run All; report any other configurations already tried. Reproduction is not a new experimental choice.

The base results are already available. Before running your additional candidate for the first time, record its expected effect in `experiment_spec.md`. Keep that expectation after the run and explain what happened in the notebook. If you already ran the candidate, state this and present the explanation as retrospective. Do not invent an earlier prediction or commit history. A wrong expectation can receive full credit when the reasoning and reflection are sound.

## Read the same decision protocol correctly

Every candidate uses the same threshold-selection rule on development: at most 10% of opportunities may trigger an alert; maximise distinct eligible pit entries detected, with precision and threshold as tie-breakers. The selected threshold may differ between candidates. Compare the resulting model and alert policy; do not attribute every change in alerts to the model parameter alone. Ties can leave some budget unused. Never alert is the reference with zero alerts.

The primary measure is event recall: distinct eligible entries caught / distinct eligible entries represented by positive opportunities. Precision is TP / alerts and is undefined when there are no alerts. Multiple positive windows can refer to one entry. The notebook starts with a small illustrative check and a compact development table; the complete table also contains TP, FP, FN, TN, alert rate, thresholds and both event counts. AP is optional supplementary evidence.

Reuse each candidate's development-selected threshold unchanged on train. The 10% budget is for development only. Train metrics are in-sample; development was used for threshold selection and comparison. Neither is an untouched final test. A train/dev gap alone does not prove its cause. A score is not demonstrated to be a calibrated probability.

## Examine three failure patterns without changing the experiment

After the additional run, “5. Explain three distinct failure patterns” shows your candidate's development predictions and descriptive tables by compound and circuit. You may inspect other permitted context columns in that same exported table. Keep the candidate and its threshold frozen; this step describes errors and does not select another model or segment-specific threshold.

In the notebook, complete three short entries. For each, state: the error type and context rule, an error count with its relevant denominator, at least one `opportunity_id` from the exported predictions, the operational consequence and one useful next check. Explain whether a proposed cause is observed or only a hypothesis. Three isolated examples of the same pattern do not constitute three modes of failure. Patterns may overlap; state this and do not sum their counts as distinct errors. A small subgroup is a limitation, not proof of a general effect. Never invent a pattern to fill the table; if evidence is insufficient, document what you checked and flag the gap.

Choose the denominator that answers your question: FP/alerts is the fraction of alerts that are false; FP/(FP+TN) is FPR over negative windows; FN/(TP+FN) is `miss_rate` over positive windows. A zero denominator is undefined. Section 5 includes a denominator dictionary, a worked fictional entry and editable queries for context/error and whole-event checks.

The same error type in different contexts can count as separate patterns when each entry states its context rule, gives its own count/denominator and traceable case, and explains a consequence and next check. Three cases of the same error in the same context count as one pattern. Changing only a context name without evidence and interpretation is incomplete. You do not need three different causes, independent groups or statistical significance. Declare overlap; do not add overlapping counts as distinct errors.

These are window-level context tables: `positive_windows` counts positive opportunities, not distinct entries. A false alert is an FP window. A missed event requires checking that none of its positive windows was alerted; a single FN window is not enough. Use the supplied event table to check this distinction.

## Write the memo for its reader

Write `memo.md` for a Head of Strategy who understands racing but does not know ML. At most one printed page, using normal margins and readable 11–12 pt text; about 400 words is a guide, not a guarantee of one page. No PDF is required: check print preview and submit the Markdown source. The optional sentence frame in the template helps organise the argument without deciding it for you.

Explain what decision the alert could support, compare actual results with denominators, recommend use/further checking/deferral, state a concrete limitation and propose a next check. Select the most relevant finding; the three full error entries stay in the notebook. Do not claim positions gained, seconds saved, causal effects or calibrated probabilities from these results. Grammar is not graded. Short notebook reasoning may be in English or Spanish; memo and code labels should be readable in English. See `GLOSSARY.md`.

## Common AI audit and truthful use record

An assistant recommends:

> Use the 2026 results to choose the forest setting and alert threshold. Then report that same 2026 score as an independent final test, because the training data still end in 2021.

In `PROMPTS.md`, respond in at most five short lines: accept/reject, methodological reason and a precise checkable cell/function/output in your own repository. This audit is required even if you used no AI. Do not obtain or run 2026 data to answer.

Also record the tool used or “No AI used for this lab”. If used, connect one actual suggestion with what you accepted/rejected, the exact verification and notebook evidence, and a relevant limitation. Do not invent a failed suggestion or interaction. Both contributors must name a concrete action and related file/cell. A truthful no-use record can earn full use-record points; there is no prompt quota.

## What is supplied and what you submit

| Kind | Files or work | Your responsibility |
|---|---|---|
| Supplied | Data CSV/manifest, support modules, requirements, brief, rubric, glossary and checklist | Keep the supplied data and protocol; use relative paths. |
| Complete | Notebook reasoning cells, `experiment_spec.md`, `memo.md`, `PROMPTS.md`, environment/run instructions in `README.md` | Supply your reasoning and record your actual work. |
| Generated | `comparison_table.md`; `outputs/comparison_v3.csv`, `run_manifest_v3.json`, `development_predictions_v3.csv`, `context_errors_v3.csv`, `event_errors_v3.csv` | Run the export block under “5. Explain three distinct failure patterns”, inspect them and commit the current files. Do not transcribe the comparison manually. |

Commit the executed notebook and all required supplied, completed and generated files. The starter contains five systems/ten rows and empty extra-candidate error exports. A completed run contains six systems/twelve rows and your candidate's error evidence. `experiment_complete: true` confirms that the additional run occurred; it does not certify the accuracy of your interpretation or the completion of your texts.

Canvas provides the official timestamp. Submit both names, accessible GitHub URL, final commit and notebook path. Check instructor access to that exact commit before the deadline; an invitation still awaiting acceptance is not verified access.

## Rubric and feedback

| Criterion | Points | Evidence you must make visible |
|---|---:|---|
| C1 Valid comparison | 25 | Valid timing/inputs; one controlled candidate; correct policy and denominators. |
| C2 Technical reasoning | 35 | Mechanism tied to base/change numbers; three supported failure patterns; bounded recommendation and limits. |
| C3 Memo for its audience | 15 | Accurate evidence translated into a concise, understandable recommendation and next check. |
| C4 Reproducibility | 15 | Accessible commit, fresh run and agreement across the submitted artefacts. |
| C5 Traceability and critical AI use | 10 | Common audit 5; truthful use/no-use and verification 3; concrete contributions 2. |

See `RUBRIC_Lab03_v3.md` for components and anchors. A supplied table, manifest or polished log does not automatically earn the strongest band. A losing additional model can earn full marks.

Before submitting, use the ungraded “Use your feedback next time” cell to revisit one relevant comment from Lab 2, or identify a weakness yourself if no comment applies. After grading, use the concrete next action in your Lab 3 feedback to improve the capstone experiment plan. No additional oral interview is part of this lab.
