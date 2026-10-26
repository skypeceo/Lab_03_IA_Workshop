"""Fixed Lab 3 protocol. No downloads and no test-period access."""
from pathlib import Path
import hashlib
import json
import platform
import importlib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from pitwindow_student_v2 import (
    FEATURES, NUMERIC, _check_train, fit_historical_baseline,
    score_historical_baseline, choose_threshold, apply_policy,
)

SEED = 414
BUDGET = 0.10
DATA_HASH = '6782cfca5940fbe7683c8b03cdb8e5a9f2990f426dc7b8f3182eec32cd7f0b3f'
ALLOWED_CHANGES = {
    ('tree', 'max_depth', 6): 3,
    ('forest_sqrt', 'max_depth', 3): 6,
    ('forest_sqrt', 'min_samples_leaf', 100): 30,
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_learning(root=Path('.')):
    root = Path(root)
    path = root / 'data' / 'learning_v2.csv'
    if not path.is_file():
        raise FileNotFoundError('Extract the complete student ZIP; data/learning_v2.csv is required.')
    if sha256(path) != DATA_HASH:
        raise ValueError('Dataset hash changed. Restore learning_v2.csv from the supplied ZIP.')
    data = pd.read_csv(path, dtype={'circuit_id': str, 'driver_id': str})
    required = set(FEATURES + ['partition', 'year', 'round_number', 'y', 'event_id', 'opportunity_id'])
    if not required.issubset(data.columns):
        raise ValueError('Missing required dataset columns.')
    if len(data) != 72616 or not data.opportunity_id.is_unique:
        raise ValueError('Unexpected rows or duplicated opportunities.')
    if set(data.partition) != {'train', 'development'} or not set(data.y.unique()) <= {0, 1}:
        raise ValueError('Unexpected partition or target.')
    train = data.loc[data.partition.eq('train')].reset_index(drop=True)
    dev = data.loc[data.partition.eq('development')].reset_index(drop=True)
    if not (train.year.between(2018, 2021).all() and
            dev.year.eq(2022).all() and dev.round_number.le(11).all()):
        raise ValueError('Temporal partition contract failed.')
    if not data.loc[data.y.eq(1), 'event_id'].notna().all():
        raise ValueError('Positive opportunities require an event identifier for auditing.')
    return train, dev


def _pipeline(model):
    numeric = Pipeline([
        ('impute', SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True)),
        ('scale', 'passthrough'),
    ])
    categorical = Pipeline([
        ('impute', SimpleImputer(strategy='constant', fill_value='UNKNOWN')),
        ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    prep = ColumnTransformer([
        ('numeric', numeric, NUMERIC),
        ('categorical', categorical, ['circuit_id', 'compound']),
    ])
    return Pipeline([('prep', prep), ('model', model)])


def fit_base_models(train):
    _check_train(train)
    forest_args = dict(n_estimators=150, max_depth=6, min_samples_leaf=30,
                       class_weight='balanced_subsample', random_state=SEED, n_jobs=2)
    models = {
        'tree': DecisionTreeClassifier(max_depth=3, min_samples_leaf=50,
                                       class_weight='balanced', random_state=SEED),
        'forest_all': RandomForestClassifier(max_features=1.0, **forest_args),
        'forest_sqrt': RandomForestClassifier(max_features='sqrt', **forest_args),
    }
    return {name: _pipeline(model).fit(train[FEATURES], train.y.astype(int))
            for name, model in models.items()}


def metrics(table, scores, policy, model_id, split):
    scores = np.asarray(scores, dtype=float)
    alert = apply_policy(scores, policy)
    y = table.y.to_numpy(dtype=int)
    tp, fp = int(np.sum(alert & (y == 1))), int(np.sum(alert & (y == 0)))
    fn, tn = int(np.sum(~alert & (y == 1))), int(np.sum(~alert & (y == 0)))
    events = int(table.loc[table.y.eq(1), 'event_id'].nunique())
    caught = int(table.loc[alert & (y == 1), 'event_id'].nunique())
    alerts = int(alert.sum())
    return dict(model=model_id, split=split, n=len(table), positive_windows=int(y.sum()),
                TP=tp, FP=fp, FN=fn, TN=tn, alerts=alerts, alert_rate=alerts / len(table),
                precision=tp / alerts if alerts else np.nan,
                window_recall=tp / int(y.sum()) if y.sum() else np.nan,
                events_caught=caught, eligible_events=events,
                event_recall=caught / events if events else np.nan,
                threshold=policy['threshold'], no_alerts=policy['no_alerts'],
                AP=float(average_precision_score(y, scores)))


def evaluate_scores(model_id, train, dev, train_scores, dev_scores, never_alert=False):
    policy = (dict(threshold=None, no_alerts=True) if never_alert
              else choose_threshold(dev_scores, dev, budget=BUDGET))
    rows = [metrics(train, train_scores, policy, model_id, 'train'),
            metrics(dev, dev_scores, policy, model_id, 'dev')]
    if rows[1]['alerts'] > int(np.floor(BUDGET * len(dev) + 1e-9)):
        raise AssertionError('Development alert budget exceeded.')
    return rows, policy


def run_base_comparison(train, dev):
    _check_train(train)
    if not dev.partition.eq('development').all():
        raise ValueError('Threshold selection requires development rows only.')
    fitted = fit_base_models(train)
    historical = fit_historical_baseline(train)
    scores = {
        'never_alert': (np.full(len(train), train.y.mean()), np.full(len(dev), train.y.mean())),
        'historical_baseline': (score_historical_baseline(train, historical),
                                score_historical_baseline(dev, historical)),
    }
    for name, model in fitted.items():
        scores[name] = (model.predict_proba(train[FEATURES])[:, 1],
                        model.predict_proba(dev[FEATURES])[:, 1])
    rows, policies = [], {}
    for name, (train_scores, dev_scores) in scores.items():
        pair, policies[name] = evaluate_scores(name, train, dev, train_scores, dev_scores,
                                               never_alert=name == 'never_alert')
        rows.extend(pair)
    return pd.DataFrame(rows), fitted, policies


def run_one_change(train, dev, fitted, model_id, parameter, new_value):
    _check_train(train)
    if not dev.partition.eq('development').all():
        raise ValueError('Threshold selection requires development rows only.')
    key = (model_id, parameter, new_value)
    if key not in ALLOWED_CHANGES:
        raise ValueError('Choose exactly one allowed model/parameter/value tuple from the brief.')
    parent = fitted[model_id]
    old_value = ALLOWED_CHANGES[key]
    if parent.get_params()[f'model__{parameter}'] != old_value:
        raise ValueError('The base model was modified; restore the supplied configuration.')
    candidate = clone(parent).set_params(**{f'model__{parameter}': new_value})
    changed = [name for name, value in parent.get_params().items()
               if name.startswith('model__') and candidate.get_params()[name] != value]
    if changed != [f'model__{parameter}']:
        raise AssertionError('More than one model parameter changed.')
    candidate.fit(train[FEATURES], train.y.astype(int))
    name = f'{model_id}__{parameter}_{new_value}'
    rows, policy = evaluate_scores(name, train, dev,
                                  candidate.predict_proba(train[FEATURES])[:, 1],
                                  candidate.predict_proba(dev[FEATURES])[:, 1])
    change = dict(parent=model_id, parameter=parameter, old=old_value, new=new_value,
                  model_id=name, changed_parameters=changed)
    return pd.DataFrame(rows), candidate, policy, change


def export_run(comparison, policies, change=None, root=Path('.'), predictions=None):
    root = Path(root)
    out = root / 'outputs'
    out.mkdir(exist_ok=True)
    comparison.to_csv(out / 'comparison_v3.csv', index=False)
    (root / 'comparison_table.md').write_text(markdown_table(comparison), encoding='utf-8')
    predictions = pd.DataFrame(columns=PREDICTION_COLUMNS) if predictions is None else predictions
    context = context_error_summary(predictions)
    events = event_error_summary(predictions)
    predictions.to_csv(out / 'development_predictions_v3.csv', index=False)
    context.to_csv(out / 'context_errors_v3.csv', index=False)
    events.to_csv(out / 'event_errors_v3.csv', index=False)
    manifest = dict(
        protocol='Lab03 v3', seed=SEED, development_budget=BUDGET,
        experiment_complete=change is not None, change=change,
        completion_note='Execution only; reasoning, error analysis and memo must be checked separately',
        generated_sha256={name: sha256(out / name) for name in
                          ['development_predictions_v3.csv', 'context_errors_v3.csv', 'event_errors_v3.csv']},
        comparison_markdown_sha256=sha256(root / 'comparison_table.md'),
        learning_sha256=sha256(root / 'data' / 'learning_v2.csv'),
        comparison_sha256=sha256(out / 'comparison_v3.csv'),
        support_sha256={name: sha256(root / name)
                        for name in ['lab03_support_v3.py', 'pitwindow_student_v2.py']},
        features=FEATURES, threshold_selection='dev only; reused unchanged on train',
        policies=policies, python=platform.python_version(),
        versions={name: importlib.import_module(module).__version__
                  for name, module in [('numpy', 'numpy'), ('pandas', 'pandas'),
                                       ('scikit-learn', 'sklearn'), ('joblib', 'joblib')]},
    )
    (out / 'run_manifest_v3.json').write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding='utf-8')
    return manifest


def markdown_table(frame):
    """Standalone table text without requiring the optional tabulate package."""
    def value(x):
        if pd.isna(x):
            return 'undefined'
        return f'{x:.6f}' if isinstance(x, (float, np.floating)) else str(x)
    lines = ['| ' + ' | '.join(frame.columns) + ' |',
             '| ' + ' | '.join(['---'] * len(frame.columns)) + ' |']
    lines += ['| ' + ' | '.join(value(x) for x in row) + ' |'
              for row in frame.itertuples(index=False, name=None)]
    return '\n'.join(lines) + '\n'


# Descriptive diagnostics below do not refit, retune or choose thresholds.
PREDICTION_COLUMNS = ['opportunity_id', 'race_id', 'driver_id', 'lap_number', 'circuit_id',
                      'compound', 'tyre_life', 'progress', 'event_id', 'y', 'model',
                      'score', 'alert', 'error_type']
CONTEXT_COLUMNS = ['dimension', 'context', 'n', 'positive_windows', 'alerts', 'TP', 'FP',
                   'FN', 'TN', 'precision', 'miss_rate']
EVENT_COLUMNS = ['event_id', 'race_id', 'driver_id', 'positive_windows',
                 'alerted_positive_windows', 'caught', 'missed_event']


def development_predictions(dev, model, policy, model_id):
    if not dev.partition.eq('development').all():
        raise ValueError('Error evidence requires development only.')
    result = dev[PREDICTION_COLUMNS[:10]].copy().reset_index(drop=True)
    result['model'] = model_id
    result['score'] = model.predict_proba(dev[FEATURES])[:, 1]
    result['alert'] = apply_policy(result.score, policy)
    positive = result.y.eq(1).to_numpy()
    alert = result.alert.to_numpy()
    result['error_type'] = np.select([alert & positive, alert & ~positive,
                                      ~alert & positive], ['TP', 'FP', 'FN'], default='TN')
    return result[PREDICTION_COLUMNS]


def context_error_summary(predictions):
    rows = []
    if predictions.empty:
        return pd.DataFrame(columns=CONTEXT_COLUMNS)
    for dimension in ['compound', 'circuit_id']:
        for context, group in predictions.groupby(dimension, dropna=False, sort=True):
            counts = group.error_type.value_counts()
            tp, fp, fn, tn = [int(counts.get(name, 0)) for name in ['TP', 'FP', 'FN', 'TN']]
            rows.append(dict(dimension=dimension, context=str(context), n=len(group),
                             positive_windows=tp+fn, alerts=tp+fp, TP=tp, FP=fp, FN=fn, TN=tn,
                             precision=tp/(tp+fp) if tp+fp else np.nan,
                             miss_rate=fn/(tp+fn) if tp+fn else np.nan))
    return pd.DataFrame(rows, columns=CONTEXT_COLUMNS)


def event_error_summary(predictions):
    rows = []
    if predictions.empty:
        return pd.DataFrame(columns=EVENT_COLUMNS)
    positives = predictions.loc[predictions.y.eq(1)]
    for event_id, group in positives.groupby('event_id', sort=True):
        alerted = int(group.alert.sum())
        rows.append(dict(event_id=event_id, race_id=group.race_id.iloc[0],
                         driver_id=group.driver_id.iloc[0], positive_windows=len(group),
                         alerted_positive_windows=alerted, caught=bool(alerted),
                         missed_event=not bool(alerted)))
    return pd.DataFrame(rows, columns=EVENT_COLUMNS)


def context_query(predictions, column, value, error_kind='FP'):
    """Summarise the FULL context, then show the requested errors; never fit or retune."""
    allowed = {'compound', 'circuit_id', 'race_id', 'driver_id', 'lap_number', 'tyre_life', 'progress'}
    if column not in allowed:
        raise ValueError('Choose a supplied context column: ' + ', '.join(sorted(allowed)))
    if error_kind not in {'FP', 'FN', 'TP', 'TN'}:
        raise ValueError('error_kind must be FP, FN, TP or TN')
    context = predictions.loc[predictions[column].eq(value)].copy()
    counts = {label: int(context.error_type.eq(label).sum()) for label in ['TP','FP','FN','TN']}
    tp, fp, fn, tn = (counts[k] for k in ['TP','FP','FN','TN'])
    ratio = lambda numerator, denominator: numerator / denominator if denominator else np.nan
    summary = pd.DataFrame([dict(context_column=column, context_value=value, n=len(context), **counts,
        alerts=tp+fp, negative_windows=fp+tn, positive_windows=tp+fn,
        false_alert_fraction=ratio(fp,tp+fp), false_positive_rate=ratio(fp,fp+tn),
        miss_rate=ratio(fn,tp+fn))])
    cases = context.loc[context.error_type.eq(error_kind), PREDICTION_COLUMNS]
    return summary, cases


def positive_windows_for_event(predictions, event_id):
    """Return every positive opportunity of one event, without a context filter."""
    return predictions.loc[predictions.y.eq(1) & predictions.event_id.eq(event_id),
        PREDICTION_COLUMNS].sort_values('opportunity_id').copy()
