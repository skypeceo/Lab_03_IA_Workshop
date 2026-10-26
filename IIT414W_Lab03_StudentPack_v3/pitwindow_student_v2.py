FEATURES = ['circuit_id', 'compound', 'tyre_life', 'lap_number', 'progress', 'prior_pit_entries', 'pace_median_s', 'pace_slope_s_per_lap', 'pace_n']
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
NUMERIC = FEATURES[2:]

def _check_train(train):
    if not train.partition.eq('train').all() or train.y.nunique() != 2:
        raise ValueError('fit requires train only and both classes')

def _baseline_keys(table):
    keys = table[['circuit_id', 'compound', 'tyre_life']].copy()
    keys[['circuit_id', 'compound']] = keys[['circuit_id', 'compound']].fillna('UNKNOWN').astype(str)
    keys['age'] = np.floor(pd.to_numeric(keys.tyre_life, errors='coerce') / 5).clip(upper=12).fillna(-1).astype(int)
    return keys

def fit_historical_baseline(train):
    _check_train(train)
    keys = _baseline_keys(train)
    keys['y'] = train.y.to_numpy(dtype=int)
    global_rate = float(keys.y.mean())
    parent = {}
    for key, g in keys.groupby(['compound', 'age']):
        parent[key] = float((g.y.sum() + 30 * global_rate) / (len(g) + 30))
    cell = {}
    for key, g in keys.groupby(['circuit_id', 'compound', 'age']):
        cell[key] = float((g.y.sum() + 30 * parent[key[1:]]) / (len(g) + 30))
    return {'global_rate': global_rate, 'parent': parent, 'cell': cell}

def score_historical_baseline(table, fitted):
    result = []
    for r in _baseline_keys(table).itertuples():
        parent = fitted['parent'].get((r.compound, r.age), fitted['global_rate'])
        result.append(fitted['cell'].get((r.circuit_id, r.compound, r.age), parent))
    return np.array(result)

def fit_candidates(train):
    _check_train(train)
    estimators = {'logistic': LogisticRegression(C=1, class_weight='balanced', max_iter=3000, random_state=414), 'tree': DecisionTreeClassifier(max_depth=3, min_samples_leaf=50, class_weight='balanced', random_state=414), 'forest_all': RandomForestClassifier(n_estimators=150, max_depth=6, min_samples_leaf=30, max_features=1.0, class_weight='balanced_subsample', random_state=414, n_jobs=2), 'forest_sqrt': RandomForestClassifier(n_estimators=150, max_depth=6, min_samples_leaf=30, max_features='sqrt', class_weight='balanced_subsample', random_state=414, n_jobs=2), 'boost': GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=2, min_samples_leaf=30, random_state=414)}
    fitted = {}
    for name, model in estimators.items():
        numeric = Pipeline([('impute', SimpleImputer(strategy='median', add_indicator=True, keep_empty_features=True)), ('scale', StandardScaler() if name == 'logistic' else 'passthrough')])
        categorical = Pipeline([('impute', SimpleImputer(strategy='constant', fill_value='UNKNOWN')), ('encode', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])
        prep = ColumnTransformer([('numeric', numeric, NUMERIC), ('categorical', categorical, ['circuit_id', 'compound'])])
        fitted[name] = Pipeline([('prep', prep), ('model', model)]).fit(train[FEATURES], train.y.astype(int))
    return fitted

def choose_threshold(scores, labels, budget=0.1):
    scores = np.asarray(scores)
    labels = labels.reset_index(drop=True)
    if len(scores) != len(labels) or not np.isfinite(scores).all():
        raise ValueError('invalid scores')
    best = {'threshold': None, 'no_alerts': True, 'alerts': 0, 'TP': 0, 'FP': 0, 'events_caught': 0, 'event_recall': 0.0}
    best_key = (0, 0.0, float('inf'))
    order = np.argsort(-scores, kind='stable')
    seen = set()
    tp = 0
    pos = 0
    limit = int(np.floor(len(scores) * budget + 1e-09))
    total = labels.loc[labels.y.eq(1), 'event_id'].nunique()
    while pos < len(order):
        end = pos + 1
        while end < len(order) and scores[order[end]] == scores[order[pos]]:
            end += 1
        if end > limit:
            break
        for idx in order[pos:end]:
            if labels.iloc[idx].y == 1:
                tp += 1
                e = labels.iloc[idx].event_id
                if pd.notna(e):
                    seen.add(e)
        threshold = float(scores[order[pos]])
        key = (len(seen), tp / end, threshold)
        if key > best_key:
            best_key = key
            best = dict(threshold=threshold, no_alerts=False, alerts=end, TP=tp, FP=end - tp, events_caught=len(seen), event_recall=len(seen) / total if total else 0.0)
        pos = end
    return best

def apply_policy(scores, policy):
    return np.zeros(len(scores), dtype=bool) if policy['no_alerts'] else np.asarray(scores) >= policy['threshold']
