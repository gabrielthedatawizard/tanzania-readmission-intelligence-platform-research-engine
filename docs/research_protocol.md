# TRIP Research Protocol

## Project Title

TRIP — Tanzania Readmission Intelligence Platform

## Study Type

Retrospective predictive modelling study using secondary health data.

## Research Domain

Health Data Science, Clinical Prediction Modelling, Machine Learning,
Biostatistics, Digital Health and Clinical Decision Support.

---

## 1. Background

Hospital readmission is an important indicator of healthcare utilization,
continuity of care, disease burden and post-discharge outcomes.

Patients may return to hospital because of disease progression, complications,
inadequate follow-up, medication-related problems, social factors or other
clinical and health-system factors.

Predictive analytics may help identify patients at increased risk of
readmission before discharge.

TRIP investigates whether routinely available patient and hospital encounter
information can support hospital readmission risk stratification.

The initial development phase will use an openly available international
dataset before later investigating adaptation and validation within the
Tanzanian healthcare context.

---

## 2. Primary Research Question

Can routinely available patient and hospital encounter information be used to
predict whether a patient will be readmitted to hospital within 30 days of
discharge?

---

## 3. Secondary Research Questions

1. Which patient and encounter characteristics are associated with 30-day
   readmission?

2. How does an interpretable statistical model such as logistic regression
   compare with machine-learning methods?

3. How well calibrated are the prediction models?

4. Does predictive performance differ across demographic groups?

5. Which predictors contribute most strongly to model predictions?

6. How might a hospital readmission intelligence platform eventually be
   adapted for use within the Tanzanian healthcare system?

---

## 4. Study Objectives

### Primary Objective

Develop and internally evaluate prediction models for 30-day hospital
readmission.

### Secondary Objectives

- Perform comprehensive exploratory data analysis.
- Investigate missing data and data quality.
- Identify predictors associated with readmission.
- Develop a logistic regression baseline model.
- Develop machine-learning models including Random Forest and XGBoost.
- Compare model discrimination and calibration.
- Assess subgroup model performance.
- Apply explainability techniques.
- Develop a prototype readmission intelligence dashboard.
- Investigate requirements for future Tanzanian adaptation and validation.

---

## 5. Initial Data Source

The initial development dataset is:

Diabetes 130-US Hospitals for Years 1999–2008

Source:
UCI Machine Learning Repository.

Dataset DOI:
10.24432/C5230J

The dataset contains hospital encounters involving patients diagnosed with
diabetes across multiple US hospitals.

This dataset will be used for methodological development and training.

Results obtained from this dataset will NOT be presented as evidence of model
performance in Tanzanian patients.

---

## 6. Study Population

Hospital encounters involving patients diagnosed with diabetes contained in
the UCI Diabetes 130-US Hospitals dataset.

### Unit of Analysis

Hospital encounter.

Important:

Multiple encounters may belong to the same patient.

The modelling strategy must therefore account for the possibility that
records from the same patient could occur more than once.

---

## 7. Outcome

### Primary Outcome

Hospital readmission within 30 days of discharge.

### Binary Target

readmission_30d = 1

if:

readmitted == "<30"

Otherwise:

readmission_30d = 0

for:

readmitted == ">30"
or
readmitted == "NO"

This outcome definition must be documented and implemented consistently.

---

## 8. Candidate Predictors

Candidate predictors may include:

- age
- sex
- race
- admission type
- admission source
- discharge disposition
- time in hospital
- number of procedures
- number of medications
- number of laboratory procedures
- number of outpatient visits
- number of emergency visits
- number of previous inpatient visits
- primary diagnosis
- secondary diagnosis
- additional diagnoses
- HbA1c measurement/result
- glucose measurement/result
- insulin treatment
- diabetes medication status
- medication changes

Predictors must only use information that would reasonably be available at the
intended prediction time.

---

## 9. Prediction Time

Initial prediction time:

At or immediately before discharge from the index hospital admission.

Variables unavailable until after discharge must not be used as predictors.

---

## 10. Exclusion Criteria

Potential exclusions will be evaluated during cohort construction.

Examples may include:

- invalid or missing patient identifiers
- encounters with unusable outcome information
- deaths where readmission is no longer a meaningful outcome
- discharge dispositions that make readmission interpretation inappropriate
- duplicated records
- records with major data integrity problems

Every exclusion must be justified and documented.

The number of records removed at each stage will be reported.

---

## 11. Missing Data

The study will:

1. quantify missingness for every variable
2. investigate patterns of missing data
3. identify variables with extreme missingness
4. distinguish structural missingness from ordinary missing values
5. avoid replacing missing values arbitrarily
6. compare suitable handling approaches

Potential approaches include:

- explicit missing category for selected categorical variables
- median or other statistically appropriate imputation
- model-based imputation
- removal of variables where missingness makes them unsuitable

Missing-data decisions will be documented before final model evaluation.

---

## 12. Data Leakage Prevention

Predictors must not contain information that becomes available only after the
readmission outcome or after the intended prediction time.

Data preprocessing must also avoid leakage.

For example:

- imputation parameters
- encoding
- scaling
- feature selection

must be learned from the training data and then applied to evaluation data.

---

## 13. Data Splitting Strategy

Because the dataset may contain repeated encounters from the same patient,
ordinary random row-level splitting could allow encounters from the same
person to appear in both training and evaluation sets.

The preferred strategy will therefore investigate splitting by patient ID.

No patient should appear in both training and test sets where feasible.

Initial split:

Training:
approximately 70%

Validation:
approximately 15%

Test:
approximately 15%

The final split strategy will be documented after examining the dataset.

---

## 14. Exploratory Data Analysis

EDA will include:

- dataset dimensions
- duplicate records
- variable types
- missingness
- class distribution
- patient age distribution
- sex distribution
- race distribution
- admission characteristics
- discharge characteristics
- length of stay
- previous healthcare utilization
- medication characteristics
- diagnosis groups
- readmission by demographic group
- readmission by clinical characteristics
- correlation and association analysis

EDA will be performed using both Python and R.

---

## 15. Statistical Analysis

Potential analyses include:

- descriptive statistics
- frequency distributions
- cross-tabulations
- chi-square tests
- comparison of continuous variables
- confidence intervals
- univariable logistic regression
- multivariable logistic regression

Statistical significance will not be treated as equivalent to clinical
importance.

Effect estimates and uncertainty will be reported where appropriate.

---

## 16. Model Development

### Baseline Model

Logistic Regression

### Machine-Learning Models

- Random Forest
- XGBoost

Additional models may be considered later.

The initial aim is not to maximize model complexity.

The aim is to compare transparent statistical modelling with more flexible
machine-learning methods.

---

## 17. Model Performance

The following metrics will be evaluated:

### Discrimination

- ROC-AUC
- Precision-Recall AUC

### Classification

- sensitivity
- specificity
- precision
- recall
- F1 score
- confusion matrix

### Calibration

- calibration plot
- calibration intercept
- calibration slope
- Brier score

Model performance will not be summarized using accuracy alone.

---

## 18. Decision Thresholds

A probability threshold will not automatically be set to 0.50.

Thresholds will be investigated according to their effect on:

- sensitivity
- specificity
- false negatives
- false positives

Future clinical thresholds would require clinical and operational input.

---

## 19. Explainability

Model interpretability approaches may include:

- logistic regression coefficients
- odds ratios
- feature importance
- SHAP values
- local patient-level explanations
- global feature importance

Explainability methods will not be interpreted as proof of causality.

---

## 20. Subgroup and Fairness Evaluation

Performance will be examined across relevant subgroups where sample sizes
permit.

Potential groups include:

- sex
- age group
- race/ethnicity categories

Potential comparisons include:

- AUROC
- sensitivity
- specificity
- calibration
- false-negative rates
- false-positive rates

Observed differences will be reported rather than automatically labelled as
algorithmic discrimination.

---

## 21. Internal Validation

The initial project will perform internal model evaluation using held-out data
and/or resampling approaches where appropriate.

Hyperparameter selection must not use the final test set.

The final test dataset should be used only after model development decisions
have been completed.

---

## 22. External Validation

External clinical validation is outside the initial UCI development phase.

A model trained using US hospital data cannot automatically be considered
valid for Tanzania.

Future work should evaluate the model using independent Tanzanian hospital
data before clinical use.

---

## 23. Tanzania Adaptation

Future Tanzania-specific research should investigate:

- availability of suitable patient-level hospital data
- differences in disease patterns
- referral pathways
- hospital infrastructure
- healthcare utilization patterns
- data completeness
- coding practices
- discharge procedures
- socioeconomic factors
- health insurance/payment structures
- digital health infrastructure

The model may require recalibration or complete retraining on local data.

---

## 24. Ethical Considerations

The initial UCI dataset is de-identified and publicly available.

Future work using identifiable or locally collected patient-level data would
require appropriate:

- ethical review
- institutional approval
- data governance
- privacy protection
- access control
- security safeguards
- data-use agreements

Clinical deployment would require substantially stronger validation and
governance than this research prototype.

---

## 25. Intended Use

TRIP is initially a research and educational prototype.

Potential future intended use:

Risk stratification and clinical decision support to assist healthcare
professionals in identifying patients who may benefit from additional
post-discharge attention.

TRIP is not intended to autonomously diagnose disease or prescribe treatment.

---

## 26. Reporting Standards

The study will be designed and documented with reference to:

- TRIPOD+AI
- PROBAST+AI

Additional reporting and clinical AI guidelines may be incorporated as the
project progresses.

---

## 27. Reproducibility

The project will maintain:

- version-controlled source code
- reproducible notebooks
- documented datasets
- data dictionaries
- environment specifications
- model configurations
- evaluation results
- research decisions
- Git commit history

GitHub will serve as the primary version-control and project documentation
platform.

---

## 28. Current Research Phase

M1 — Research Protocol and Dataset Understanding

No final clinical model has yet been developed.
