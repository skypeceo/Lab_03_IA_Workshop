# Recommendation to the Head of Strategy: rival pit-entry alert

**Decision it could support.** At the end of each lap, the alert flags a rival who is likely to enter the pits during their next three laps, so the pit wall can prepare a response (cover, undercut or stay out) earlier. It predicts what the rival *will do*, not what we *should do*.

**How we tested it.** We built the alert from 2018–2021 races and compared versions on the first 11 races of 2022 (9,451 lap-end checks, 370 real pit entries). Every version could alert on at most 10% of checks (945 alerts), so they all had the same "attention budget".

**What we found (2022, first 11 races).**

| Version | Pit entries flagged in time | Alerts used | Correct alerts |
|---|---|---|---|
| Simple rule from past pit rates | 94 of 370 (25%) | 931 | 250 of 931 (27%) |
| Best version ("forest_sqrt") | **140 of 370 (38%)** | 945 | **340 of 945 (36%)** |
| Our tested change (deeper single decision tree) | 57 of 370 (15%) | 580 | 145 of 580 (25%) |

The best version flags about half again as many pit entries as the simple rule, with the same budget. Our own change made a simpler model *worse*: it caught 57 entries instead of the 63 its unchanged version caught. We do not recommend it.

**Recommendation: further checking before any race use.** Even the best version misses about 6 in 10 pit entries, and about 2 in 3 of its alerts are false. A "correct alert" means the rival pitted within three laps; it does not mean we would have gained positions or time, which we did not measure. The alert scores are rankings, not reliable probabilities.

**Main limitation.** The alert is blind in wet conditions. In the deeper tree we examined in detail, all 46 pit entries made on intermediate or wet tyres were missed: it never alerted once on those tyres. It also missed 51 of 53 entries in the Barcelona race (22 May 2022), and we do not yet know why. In addition, the 2022 races were used to choose each version's alert setting, so these results are likely optimistic.

**Next check.** Freeze the best version and its alert setting, then test them once, without changes, on races never used in development (rest of 2022 and later seasons). We would report wet and dry races separately. Only if it still detects clearly more entries than the simple rule would we suggest a trial on the pit wall, where the strategist sees the alert without acting on it.
