# Lab 3 start here

Due Thu 29 October 2026, 12:30 Santiago. Same pairs as Lab 2. 100 points, 6% NP.
Read the short route in `IIT414W_Lab03_Brief_v3.md`; criterion components are in `RUBRIC_Lab03_v3.md`.

## Choose your environment

**Already able to run the class notebook?** Start with that environment and run the block under “Environment and data check”
in `Lab03_ModelComparison_Student_v3.ipynb`. It checks the selected Python, required imports,
working directory and supplied data. Record actual versions in your final outputs and update this README
with the steps you used. If the environment fails, use the clean alternative below.

Extract the complete ZIP to a folder first. Open VS Code/Jupyter with that folder as the working directory.
Do not open the notebook inside the ZIP. Select your intended Python kernel.
The experiment makes no downloads. Installation is a separate step that may need internet.

## Clean alternative tested with Python 3.12

From a terminal in the extracted folder:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements_lab03_v3.txt
.venv\Scripts\python -m ipykernel install --user --name iit414w-lab03-v3 --display-name "IIT414W Lab03 v3"
```

On macOS/Linux use `.venv/bin/python` in place of `.venv\Scripts\python`.
Select the installed kernel in your notebook editor. The tested scientific versions are numpy 2.0.2,
pandas 2.3.1, sklearn 1.8.0, scipy 1.17.1 and joblib 1.4.2. Do not replace your whole working class
environment just to match a label; document the actual environment and investigate material differences.

## One route through the work

1. Run the environment/data check, complete “1. Define the prediction”, and try the illustrative metric check.
2. Run the five base systems and answer “2. Explain the common comparison”.
3. Complete `experiment_spec.md` BEFORE the first additional run, or declare it retrospective if already run.
4. Set the three fields in “3. Record your expectation before your additional run” (configuration block), run and answer “4. Explain your additional result”.
5. In “5. Explain three distinct failure patterns”, inspect the tables and queries, then complete “Your three entries”.
6. Complete `memo.md` and `PROMPTS.md`. Revisit earlier feedback in the ungraded “Use your feedback next time” cell.
7. Restart + Run All, save outputs and commit the entire required package. Check instructor access.

## Files you keep, complete and generate

| Supplied and retained | You complete | Notebook generates |
|---|---|---|
| Data/manifest, both Python modules, requirements, brief, rubric, glossary, checklist | Notebook answer cells, experiment_spec.md, memo.md, PROMPTS.md, actual run instructions here | comparison_table.md and five files in outputs/ |

Five base systems produce ten train/dev rows. A completed candidate adds one system/two rows,
so the final comparison has SIX systems and TWELVE rows. The starter runs without an additional candidate
and explicitly reports INCOMPLETE. Empty error-export headers in the starter are intentional.
The execution flag confirms only that the candidate ran. Your reasoning and documents must also be complete.
The Markdown table is generated: do not copy or edit its numbers manually.

## Final submission

Canvas text entry: both names, accessible GitHub repository URL, final commit ID and notebook filename.
The repository includes the executed notebook, supplied support/data files, completed documents and current exports.
Check `CHECKLIST.md`. Do not commit your `.venv`, credentials or unrelated personal files.

One additional configuration may be rerun for reproducibility. In section 5, set a context/error query and, when needed, an event query; these only inspect frozen predictions and do not fit a model. Use the denominator dictionary and fictional examples there.
