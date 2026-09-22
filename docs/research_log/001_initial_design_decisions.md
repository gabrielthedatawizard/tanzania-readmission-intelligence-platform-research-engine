# Research Decision Log 001

## Date

2026-09-22

## Decision

Use the UCI Diabetes 130-US Hospitals dataset as the first development dataset.

## Reason

The dataset contains more than 100,000 hospital encounters and includes a
readmission outcome suitable for development of a 30-day readmission
prediction pipeline.

## Important Limitation

The dataset represents US hospitals and therefore cannot establish clinical
validity for Tanzania.

## Target

Binary 30-day readmission:

1 = readmitted within 30 days
0 = not readmitted within 30 days

## Prediction Time

At or immediately before hospital discharge.

## Initial Models

1. Logistic Regression
2. Random Forest
3. XGBoost

## Evaluation Priorities

1. Discrimination
2. Calibration
3. Sensitivity
4. Specificity
5. Precision-recall performance
6. Subgroup performance

## Major Risk Identified

Multiple encounters may belong to the same patient.

Patient-level leakage must be investigated before splitting the dataset.

## Tanzania Position

The first model is a methodological baseline and not a Tanzanian clinical
model.

Future work will require independent Tanzanian data and external validation.
