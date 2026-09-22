# TRIP — Tanzania Readmission Intelligence Platform

TRIP is a health data science research project focused on hospital readmission prediction, clinical analytics, and decision support.

The project aims to explore how statistical analysis, machine learning, and health information systems can support early identification of patients at elevated risk of hospital readmission.

## Main Objectives

- Analyze hospital readmission patterns
- Build statistical and machine-learning models for 30-day readmission prediction
- Compare model performance and calibration
- Investigate subgroup performance and fairness
- Develop explainable risk predictions
- Build a clinical and population-level analytics dashboard
- Explore how the platform could be adapted to the Tanzanian healthcare context

## Research Tools

### Python
- pandas
- numpy
- matplotlib
- scikit-learn
- xgboost
- shap
- statsmodels

### R
- tidyverse
- ggplot2
- dplyr
- tidyr
- caret
- pROC

### Other Tools
- Git
- GitHub
- Jupyter
- RStudio
- SQL
- MLflow
- Power BI / Streamlit

## Project Structure

- `docs/` — research documentation and methodology
- `data/` — dataset documentation and local data folders
- `notebooks/` — exploratory and statistical analysis
- `src/` — reusable source code
- `reports/` — figures, tables, and progress reports
- `models/` — trained model artifacts
- `dashboard/` — analytics dashboard
- `tests/` — project tests

## Research Status

Current milestone:

**M1 — Research Protocol and Dataset Understanding**

## Research Roadmap

### M0 — Repository Foundation ✅

- Repository structure
- Project scope
- Git configuration

### M1 — Research Protocol 🔄

- Research questions
- Study population
- Outcome definition
- Predictor strategy
- Evaluation methodology
- Ethical framework
- Dataset documentation

### M2 — Data Acquisition & Data Dictionary

- acquire official UCI dataset
- verify dataset integrity
- document every variable
- inspect patient identifiers
- inspect missing-value codes
- create data dictionary

### M3 — Exploratory Data Analysis

- Python EDA
- R EDA
- missingness analysis
- outcome distribution
- demographic analysis
- utilization analysis
- diagnosis analysis

### M4 — Cohort & Preprocessing

- exclusion criteria
- patient-level splitting
- encoding
- missing-data handling
- feature engineering
- leakage checks

### M5 — Statistical Modelling

- univariable analyses
- logistic regression
- effect estimates
- uncertainty
- calibration

### M6 — Machine Learning

- Random Forest
- XGBoost
- hyperparameter tuning
- model comparison

### M7 — Model Evaluation

- AUROC
- PR-AUC
- sensitivity
- specificity
- Brier score
- calibration
- threshold analysis

### M8 — Explainability & Fairness

- SHAP
- global explanations
- patient explanations
- subgroup analysis

### M9 — TRIP Application Integration

- prediction API
- model packaging
- input validation
- application integration

### M10 — Dashboard

- patient intelligence
- hospital analytics
- population analytics

### M11 — Tanzania Health Data Layer

- WHO indicators
- Ministry of Health data
- DHIS2/HMIS exploration
- DHS analysis
- digital-health context

### M12 — Tanzania Validation Roadmap

- local hospital data requirements
- ethics
- partnerships
- external validation
- recalibration/retraining strategy

## Disclaimer

This project is currently a research and educational prototype.

It must not be used for clinical decision-making without appropriate clinical validation, governance, ethical approval, and regulatory review.
