# TRIP Data Sources

## DS001 — Diabetes 130-US Hospitals for Years 1999–2008

### Provider

UCI Machine Learning Repository

### Dataset DOI

10.24432/C5230J

### Dataset Type

De-identified hospital encounter data.

### Study Period

1999–2008.

### Geographic Context

United States.

### Number of Encounters

101,766.

### Number of Features

47.

### Clinical Population

Hospital encounters involving patients diagnosed with diabetes.

### Prediction-Relevant Outcome

Readmission status:

- <30
- >30
- NO

### TRIP Transformation

For the initial binary prediction problem:

<30 → 1

>30 → 0

NO → 0

### Intended TRIP Use

Baseline methodological model development.

### Strengths

- large sample
- real hospital data
- explicit readmission target
- mixed clinical and utilization variables
- suitable for classification research
- openly licensed

### Limitations

- historical data
- US healthcare context
- diabetes-focused population
- not representative of Tanzania
- categorical coding requires interpretation
- missing values are present
- repeated patients may occur
- healthcare practice may have changed since the collection period

### License

Creative Commons Attribution 4.0.

### Citation

Clore J, Cios K, DeShazo J, Strack B.
Diabetes 130-US Hospitals for Years 1999–2008.
UCI Machine Learning Repository.

DOI: 10.24432/C5230J
