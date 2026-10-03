# TRIP Data Dictionary — DS001 (M2)

Source: Diabetes 130-US Hospitals for Years 1999–2008, UCI ML Repository, DOI 10.24432/C5230J.
Files: `data/raw/diabetic_data.csv` + `data/raw/IDS_mapping.csv` (both gitignored, local only).
Verified shape: **101,766 rows × 50 columns** via `src/data/verify_dataset.py` → `reports/tables/m2_verification_summary.csv`.

Outcome (protocol §7): `readmitted` → `readmission_30d = 1` if `<30` else `0`.
Distribution: NO 54,864 / >30 35,545 / <30 11,357 (30-day rate 11.16%).

Unit of analysis: hospital encounter. **71,518 unique `patient_nbr`** for 101,766 rows; 16,773 patients have repeats (max 40). Patient-level splitting required in M4. `encounter_id` unique (0 duplicates).

## Missing-value codes (verified counts)

| Code | Columns | Count (%) |
|---|---|---|
| `?` | weight | 98,569 (96.9%) |
| `?` | medical_specialty | 49,949 (49.1%) |
| `?` | payer_code | 40,256 (39.6%) |
| `?` | race | 2,273 (2.2%) |
| `?` | diag_3 / diag_2 / diag_1 | 1,423 (1.4%) / 358 (0.4%) / 21 (0.02%) |
| NaN (empty) | max_glu_serum | 96,420 (94.7%) |
| NaN (empty) | A1Cresult | 84,748 (83.3%) |
| `Unknown/Invalid` | gender | 3 |

M2 decisions: weight, max_glu_serum, A1Cresult flagged as extreme-missingness (handle/remove in M4, do not blindly impute); `?` in race/payer/medical_specialty/diag treated as explicit missing category candidate; gender `Unknown/Invalid` (n=3) to be excluded or grouped in M4.

## Identifiers

| Column | Type | Notes |
|---|---|---|
| encounter_id | int, 101,766 unique | Row identifier, never a predictor |
| patient_nbr | int, 71,518 unique | Patient identifier, for grouping/splitting only, never a predictor |

## Demographics

| Column | Values | Notes |
|---|---|---|
| race | Caucasian 76,099; AfricanAmerican 19,210; ? 2,273; Hispanic 2,037; Other 1,506; Asian 641 | US-centric; fairness subgroup in M8 but not transferable to Tanzania |
| gender | Female 54,708; Male 47,055; Unknown/Invalid 3 | Protocol says sex; source codes gender |
| age | 10 bands [0-10) to [90-100); mode [70-80) 26,068 | Ordinal banded; top bands 70-80, 60-70, 50-60 |
| weight | ? 96.9%, else [75-100) 1,336; [50-75) 897; [100-125) 625 … | Candidate for removal in M4 |

## Encounter / utilization

| Column | Type / values | Notes |
|---|---|---|
| admission_type_id | 1 Emergency 53,990; 3 Elective 18,869; 2 Urgent 18,480; 6 NULL 5,291; 5 Not Available 4,785; 8 Not Mapped 320; 7 Trauma 21; 4 Newborn 10 | See ID map below |
| discharge_disposition_id | 26 codes; top 1 home 60,234; 3 SNF 13,954; 6 home-health 12,902; 18 NULL 3,691 … 11 Expired 1,642 | Expired/hospice codes are M4 exclusion candidates (readmission not meaningful) |
| admission_source_id | 7 ER 57,494; 1 referral 29,565; 17 NULL 6,781 … | See ID map below |
| time_in_hospital | int 1–14, mean 4.4, median 4 | Length of stay |
| payer_code | ? 39.6%; MC 32,439; HM 6,274; SP 5,007 … 15 codes | US payer, low Tanzania transferability |
| medical_specialty | ? 49.1%; InternalMedicine 14,635; Emergency/Trauma 7,565; Family/GeneralPractice 7,440 … 73 values | High-cardinality + high missing |
| num_lab_procedures | 1–132, mean 43.1 | |
| num_procedures | 0–6, mean 1.34 | |
| num_medications | 1–81, mean 16.0 | |
| number_outpatient | 0–42, mean 0.37 | Prior-year counts |
| number_emergency | 0–76, mean 0.20 | |
| number_inpatient | 0–21, mean 0.64 | Key utilization predictor |
| number_diagnoses | 1–16, mean 7.4, median 8 | |

## Diagnoses (ICD-9 coded, `?` = missing)

| Column | Top values |
|---|---|
| diag_1 | 428 heart failure 6,862; 414 ischemic 6,581; 786 respiratory 4,016; 410 AMI 3,614 … 717 codes |
| diag_2 | 276 fluid/electrolyte 6,752; 428 6,662; 250 diabetes 6,071 … 749 codes |
| diag_3 | 250 diabetes 11,555; 401 hypertension 8,289 … 790 codes + 1,423 `?` |

M4: group into clinical categories; do not use raw 700+ levels directly.

## Labs

| Column | Values | Missing |
|---|---|---|
| max_glu_serum | Norm 2,597; >200 1,485; >300 1,264 | NaN 96,420 (94.7%) — test not performed |
| A1Cresult | >8 8,216; Norm 4,990; >7 3,812 | NaN 84,748 (83.3%) — test not performed |

Distinguish “not ordered” (NaN) from measured value; candidate for missing-indicator + removal sensitivity.

## Medications (No / Steady / Up / Down; Ch = changed)

24 columns. Active: insulin (No 47,383; Steady 30,849; Down 12,218; Up 11,316), metformin (No 81,778; Steady 18,346), glipizide, glyburide, pioglitazone, rosiglitazone, glimepiride.
Near-constant (M4 removal candidates): examide (all No), citoglipton (all No), acetohexamide (1 Steady), troglitazone (3 Steady), tolbutamide (23 Steady), glimepiride-pioglitazone / metformin-pioglitazone (1 Steady each), metformin-rosiglitazone (2 Steady), glipizide-metformin (13 Steady), miglitol, tolazamide, acarbose, chlorpropamide, nateglinide.

| Column | Notes |
|---|---|
| change | No 54,755 / Ch 47,011 — any med change during stay |
| diabetesMed | Yes 78,363 / No 23,403 — any diabetes med |

## Outcome

| Column | Values | TRIP mapping |
|---|---|---|
| readmitted | NO 54,864; >30 35,545; <30 11,357 | `<30` → 1 else 0 |

## ID mappings (`IDS_mapping.csv`)

Admission type: 1 Emergency, 2 Urgent, 3 Elective, 4 Newborn, 5 Not Available, 6 NULL, 7 Trauma Center, 8 Not Mapped.
Discharge: 1 home, 2 short-term hospital, 3 SNF, 4 ICF, 5 inpatient institution, 6 home-health, 7 AMA, 8 home-IV, 9 inpatient, 10 neonatal aftercare, 11 Expired, 12 still patient, 13 hospice/home, 14 hospice/facility, 15 swing bed, 16 referred outpatient, 17 referred outpatient (this institution), 18 NULL, 19–21 expired/hospice (Medicaid), 22 rehab, 23 LTCH, 24 nursing (Medicaid-only), 25 Not Mapped, 26 Unknown/Invalid, 27 federal facility, 28 psych, 29 CAH, 30 other institution.
Source: 1 physician referral, 2 clinic, 3 HMO, 4 hospital transfer, 5 SNF, 6 other facility, 7 ER, 8 court/law, 9 Not Available, 10 critical-access transfer, 11 normal delivery, 13 sick baby, 14 extramural birth, 17 NULL, 18 home-health agency, 19 same home-health readmission, 20 Not Mapped, 21 Unknown/Invalid, 22 hospital inpatient claim, 23 born in hospital, 24 born outside, 25 ambulatory surgery, 26 hospice. (Codes 12, 15, 16 absent in data.)

## M4 handoff

Exclude/consider: expired/hospice discharges, newborn/trauma, `Unknown/Invalid` gender (n=3); drop or indicator-encode weight, max_glu_serum, A1Cresult; drop constant meds (examide, citoglipton); group diag + medical_specialty + payer_code; patient-level 70/15/15 split; leakage-safe imputation/encoding fitted on train only.
