"""M2 — Dataset acquisition verification for TRIP.

Verifies the UCI Diabetes 130-US Hospitals dataset placed at
`data/raw/diabetic_data.csv` (plus `IDS_mapping.csv`).

What it checks (per research_protocol.md M2):
 1. File exists, shape = (101766, 50)
 2. Outcome distribution: NO / >30 / <30 + derived 30-day rate
 3. Patient-level leakage risk: unique patients vs rows, repeat counts
 4. Encounter-ID uniqueness
 5. Missing-value codes: '?', 'Unknown/Invalid', NaN per column
 6. Writes a per-column summary to reports/tables/m2_verification_summary.csv

Usage (from repo root, with `trip` env active):
    python src/data/verify_dataset.py
    python src/data/verify_dataset.py --data data/raw/diabetic_data.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CANDIDATES = [
    REPO_ROOT / "data" / "raw" / "diabetic_data.csv",
    REPO_ROOT / "data" / "raw" / "diabetes+130-us+hospitals+for+years+1999-2008" / "diabetic_data.csv",
    Path(r"C:\Users\Administrator\Downloads\diabetes+130-us+hospitals+for+years+1999-2008\diabetic_data.csv"),
]

EXPECTED_ROWS = 101_766
EXPECTED_COLS = 50
EXPECTED_30D_COUNT = 11_357


def resolve_dataset(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if p.exists():
            return p
        raise FileNotFoundError(f"Dataset not found at --data={p}")
    for p in DEFAULT_CANDIDATES:
        if p.exists():
            return p
    tried = "\n  ".join(str(p) for p in DEFAULT_CANDIDATES)
    raise FileNotFoundError(
        "diabetic_data.csv not found. Tried:\n  " + tried
        + "\nCopy it to data/raw/diabetic_data.csv "
        + "(gitignored, stays local)."
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=None, help="Path to diabetic_data.csv")
    args = ap.parse_args()

    data_path = resolve_dataset(args.data)
    print(f"Dataset: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Shape: {df.shape} (expected {(EXPECTED_ROWS, EXPECTED_COLS)})")
    assert df.shape[0] == EXPECTED_ROWS, f"Row mismatch: {df.shape[0]}"
    assert df.shape[1] == EXPECTED_COLS, f"Column mismatch: {df.shape[1]}"

    # --- Outcome (protocol section 7) ---
    print("\nOutcome distribution:")
    print(df["readmitted"].value_counts())
    rate_30d = (df["readmitted"] == "<30").mean()
    n_30d = int((df["readmitted"] == "<30").sum())
    print(f"\n30-day readmission: n={n_30d} rate={rate_30d:.4f}")
    assert n_30d == EXPECTED_30D_COUNT, f"<30 count {n_30d} != {EXPECTED_30D_COUNT}"

    # --- Patient-level leakage (protocol section 13, decision log 001) ---
    n_patients = df["patient_nbr"].nunique()
    print(f"\nUnique patients: {n_patients} vs rows: {len(df)}")
    print(f"Repeat-encounter patients: {(df['patient_nbr'].value_counts() > 1).sum()}")
    print("Top repeat counts:")
    print(df["patient_nbr"].value_counts().head(5))
    assert n_patients < len(df), "Expected repeated patients (leakage risk to handle in M4)"
    dup_enc = int(df["encounter_id"].duplicated().sum())
    print(f"Duplicated encounter_id: {dup_enc}")
    assert dup_enc == 0

    # --- Missing-value codes ---
    print("\n'?' code counts (top):")
    q = (df == "?").sum().sort_values(ascending=False)
    print(q[q > 0].head(10))
    print("\nNaN counts (top):")
    na = df.isna().sum().sort_values(ascending=False)
    print(na[na > 0].head(10))

    # --- Per-column summary for data dictionary starter ---
    rows = []
    for col in df.columns:
        rows.append(
            {
                "column": col,
                "dtype": str(df[col].dtype),
                "n_unique": int(df[col].nunique()),
                "n_missing_nan": int(df[col].isna().sum()),
                "n_question_mark": int((df[col] == "?").sum()) if df[col].dtype == object else 0,
            }
        )
    out = REPO_ROOT / "reports" / "tables" / "m2_verification_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"\nWrote {out}")
    print("\nM2 verification PASSED. Next: full data dictionary + M3 EDA.")


if __name__ == "__main__":
    main()
