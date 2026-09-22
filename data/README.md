# Data Directory

This directory contains all project data files.

## Structure

- `raw/` — original, unmodified source data (gitignored)
- `interim/` — intermediate data that has been transformed (gitignored)
- `processed/` — final, analysis-ready datasets (gitignored)

## Important

Raw patient data and sensitive datasets must **never** be committed to version control.

All data subdirectories are gitignored except for `.gitkeep` placeholder files.
