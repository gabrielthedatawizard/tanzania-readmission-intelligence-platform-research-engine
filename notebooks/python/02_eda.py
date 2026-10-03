"""M3 — Exploratory Data Analysis (Python) for TRIP.

Per research_protocol.md §14. Reuses M2 verified dataset, adds encounter-level
EDA tables + figures for the M3 milestone.

Inputs: data/raw/diabetic_data.csv (gitignored)
Outputs:
  reports/tables/m3_*.csv
  reports/figures/m3_*.png

Usage (trip env, repo root):
    python notebooks/python/02_eda.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = [
    REPO_ROOT / "data" / "raw" / "diabetic_data.csv",
    REPO_ROOT / "data" / "raw" / "diabetes+130-us+hospitals+for+years+1999-2008" / "diabetic_data.csv",
    Path(r"C:\Users\Administrator\Downloads\diabetes+130-us+hospitals+for+years+1999-2008\diabetic_data.csv"),
]
TABLES = REPO_ROOT / "reports" / "tables"
FIGS = REPO_ROOT / "reports" / "figures"


def resolve() -> Path:
    for p in CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("diabetic_data.csv not found. Copy it to data/raw/.")


def rate(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(level=0)["readmission_30d"].agg(n="size", rate="mean").reset_index()
    return g


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(resolve(), low_memory=False)
    print(f"Shape: {df.shape}")
    df["readmission_30d"] = (df["readmitted"] == "<30").astype(int)

    # 1. Overall outcome
    overall = pd.DataFrame({
        "n_total": [len(df)],
        "n_30d": [int(df["readmission_30d"].sum())],
        "rate_30d": [df["readmission_30d"].mean()],
        "n_patients": [df["patient_nbr"].nunique()],
    })
    overall.to_csv(TABLES / "m3_outcome_overall.csv", index=False)
    print(overall.to_string(index=False))

    # 2. By demographics
    for col in ["age", "race", "gender"]:
        t = df.groupby(col)["readmission_30d"].agg(n="size", n_30d="sum", rate="mean").reset_index().sort_values("n", ascending=False)
        t.to_csv(TABLES / f"m3_readmit_by_{col}.csv", index=False)
        print(f"\nBy {col}:\n{t.head(12).to_string(index=False)}")

    # 3. Utilization + LOS by outcome
    util_cols = ["time_in_hospital", "num_lab_procedures", "num_procedures",
                 "num_medications", "number_outpatient", "number_emergency",
                 "number_inpatient", "number_diagnoses"]
    t = df.groupby("readmission_30d")[util_cols].mean().T
    t.columns = ["no_30d", "readmit_30d"]
    t.to_csv(TABLES / "m3_utilization_by_outcome.csv")
    print(f"\nUtilization means by outcome:\n{t.to_string()}")

    # 4. Top diagnoses
    for c in ["diag_1", "diag_2", "diag_3"]:
        t = df[c].value_counts().head(15).reset_index()
        t.columns = ["code", "n"]
        t.to_csv(TABLES / f"m3_top_{c}.csv", index=False)

    # 5. Missingness top (for M4 reference)
    miss = pd.DataFrame({
        "n_question": [(df[c] == "?").sum() if df[c].dtype == object else 0 for c in df.columns],
        "n_nan": [int(df[c].isna().sum()) for c in df.columns],
    }, index=df.columns)
    miss["pct_missing"] = (miss["n_question"] + miss["n_nan"]) / len(df)
    miss.sort_values("pct_missing", ascending=False).head(12).to_csv(TABLES / "m3_missingness_top.csv")
    print(f"\nWorst missingness:\n{miss.sort_values('pct_missing', ascending=False).head(8).to_string()}")

    # --- Figures ---
    # Outcome bar
    ax = df["readmitted"].value_counts().reindex(["NO", ">30", "<30"]).plot(kind="bar")
    ax.set_title("Outcome distribution (encounter-level, n=101,766)")
    ax.set_ylabel("Encounters")
    plt.tight_layout(); plt.savefig(FIGS / "m3_outcome_bar.png", dpi=150); plt.close()

    # Rate by age (ordered bands)
    order = ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
             "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"]
    t = df.groupby("age")["readmission_30d"].mean().reindex(order)
    t.plot(kind="bar")
    plt.title("30-day readmission rate by age band")
    plt.ylabel("Rate"); plt.tight_layout()
    plt.savefig(FIGS / "m3_readmit_by_age.png", dpi=150); plt.close()

    # Rate by race
    df.groupby("race")["readmission_30d"].mean().sort_values().plot(kind="barh")
    plt.title("30-day readmission rate by race")
    plt.xlabel("Rate"); plt.tight_layout()
    plt.savefig(FIGS / "m3_readmit_by_race.png", dpi=150); plt.close()

    # LOS distribution by outcome
    for v, label in [(0, "no_30d"), (1, "readmit_30d")]:
        plt.hist(df.loc[df["readmission_30d"] == v, "time_in_hospital"],
                 bins=range(1, 16), alpha=0.6, label=label)
    plt.title("Length of stay by 30-day outcome")
    plt.xlabel("Days"); plt.ylabel("Encounters"); plt.legend()
    plt.tight_layout(); plt.savefig(FIGS / "m3_los_by_outcome.png", dpi=150); plt.close()

    # Prior inpatient visits vs rate
    t = df.groupby("number_inpatient")["readmission_30d"].mean()
    t[t.index <= 10].plot(kind="bar")
    plt.title("30-day rate by prior inpatient visits (0-10)")
    plt.ylabel("Rate"); plt.tight_layout()
    plt.savefig(FIGS / "m3_readmit_by_prior_inpatient.png", dpi=150); plt.close()

    print(f"\nWrote tables to {TABLES / 'm3_*.csv'}")
    print(f"Wrote figures to {FIGS / 'm3_*.png'}")
    print("M3 Python EDA done. Next: review figures, then M4 cohort/split.")


if __name__ == "__main__":
    main()
