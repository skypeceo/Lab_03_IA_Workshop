# Reading the alert comparison

| Term | Meaning in this lab |
|---|---|
| Opportunity or window | One eligible prediction at the end of a rival's lap, looking ahead three of that driver's own laps. |
| Positive window | An opportunity whose label y=1: a pit entry falls inside that horizon. Several positives can refer to one event. |
| Event | One distinct observed pit entry, identified by event_id for label auditing. That future-known ID is not a predictor. |
| Alert | A window where the score meets the model's chosen rule. An alert is a prediction, not a confirmed entry. |
| TP / FP / FN / TN | Correct alert / false alert / missed positive window / correctly quiet negative window. |
| Precision | TP / alerts. Undefined if no alerts. This counts windows, not events. |
| Event recall | Distinct caught eligible entries / distinct eligible entries. Caught means at least one positive window alerted. |
| Development or dev | First eleven rounds of 2022, used to select thresholds and compare candidates. Not an untouched final test. |
| Threshold policy | A common selection procedure, not necessarily a common numeric score cutoff. |
| Parent candidate | The unmodified base model from which your one additional candidate is cloned. |
| Failure pattern | An observed kind of error in a defined context with evidence and denominators; a proposed cause remains a hypothesis unless measured. |

Historical snapshots may contain revisions and do not prove live arrival times. Tyre age is last reported
and can lag. Only entries with eligible positive opportunities enter the event denominator.
The score is not demonstrated to be a calibrated probability. No positions or seconds gained are measured.

## Choose the denominator before interpreting an error

| Question within your context | Calculation | Denominator counts |
|---|---|---|
| Of the alerts issued, how many were false? | FP / (TP + FP) | Alerted windows; false-alert fraction, equal to 1 − precision when defined. |
| Of the negative windows, how many alerted? | FP / (FP + TN) | Negative windows; false positive rate (FPR). |
| Of the positive windows, how many were quiet? | FN / (TP + FN) | Positive windows; `miss_rate` in the context export. |
| Of the eligible events, how many were completely missed? | Completely missed events / eligible events | Distinct pit entries; use all positive windows for each event. |

A zero denominator means undefined, shown as NaN; it does not mean zero errors. Name your population and unit with every fraction. Window context groups do not define an event population automatically: if describing missed events in a context, state which distinct events you include and check all their positive windows, including those outside that context. The event query below checks a whole event.
