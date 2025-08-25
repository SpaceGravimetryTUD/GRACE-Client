# grace_query/problematic.py
import pandas as pd
from dataclasses import dataclass

@dataclass
class ProblematicConfig:
    cadence_seconds: int = 5
    missing_threshold_pct: float = 2.0
    report_path: str | None = None

def diagnose(df: pd.DataFrame, time_col: str, cfg: ProblematicConfig) -> pd.DataFrame:
    s = pd.to_datetime(df[time_col]).sort_values()
    months = s.dt.to_period("M")
    out = []
    for m, g in s.groupby(months):
        start, end = pd.Timestamp(m.start_time), pd.Timestamp(m.end_time)
        expected = max(0, int((end - start).total_seconds() // cfg.cadence_seconds))
        actual = g.size
        missing_pct = 0.0 if expected == 0 else (max(expected-actual,0)/expected)*100
        out.append({"month": str(m), "expected": expected, "actual": actual,
                    "missing_pct": missing_pct, "problematic": missing_pct > cfg.missing_threshold_pct})
    return pd.DataFrame(out)