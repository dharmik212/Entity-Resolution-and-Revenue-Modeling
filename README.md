# Retail Location Matching & Revenue Estimation
## Location Matching & Revenue Analysis

This repository demonstrates an entity resolution pipeline and revenue adjustment modeling workflow using retail financial and location data.

It includes:

- **Part A:** Entity resolution (location matching) between `raw_financials` and `business_locations`
- **Part B:** Revenue adjustment methodology (estimating total revenue from card-only revenue), visualizations, and theoretical answers

---

## Repository Structure

```
/
notebooks/
01_part_a_location_matching.ipynb
01_part_a_report.ipynb
02_part_b_revenue_adjustment.ipynb
02_part_b_report.ipynb
src/
config.py
duckdb_utils.py
matching.py
data/ # not committed 
raw_financials.parquet
business_locations.parquet
outputs/
figures/
```

---

## Setup

### 1) Create and Activate a Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2) Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Data

Place the following parquet files into the `data/` folder:

```
data/raw_financials.parquet
data/business_locations.parquet
```

These correspond to the files referenced in the assessment README:

- `raw_financials.parquet`
- `business_locations.parquet`

---

## How to Run (Notebook Order)

Run the notebooks **in the following order**:

---

### 🔹 Part A — Matching Pipeline

**Notebook:**  
`notebooks/01_part_a_location_matching.ipynb`

What it does:

- Builds candidate pairs (blocking)
- Runs normalization + fuzzy matching
- Produces match outputs and financial table (CSV + Parquet)

---

### 🔹 Part A — Report / Documentation

**Notebook:**  
`notebooks/01_part_a_report.ipynb`

Includes:

- Methodology
- Assumptions
- Limitations
- Sanity checks and sample rows

---

### 🔹 Part B — Revenue Adjustment + Visuals

**Notebook:**  
`notebooks/02_part_b_revenue_adjustment.ipynb`

What it does:

- Builds baseline and segmented multiplier models
- Produces comparative plots
- Exports final adjusted financial table (CSV + Parquet)

---

### 🔹 Part B — Report / Documentation

**Notebook:**  
`notebooks/02_part_b_report.ipynb`

Includes:

- Theoretical answers (sample size + model comparison)
- Model selection rationale
- Summary of results

---

## Outputs

After running the notebooks, the following files are generated locally:

### Financial Tables

- `outputs/financial_table.csv`  
  Financial table with matched location IDs and raw card revenue (plus diagnostic columns)

- `outputs/financial_table.parquet`

- `outputs/financial_table_final.csv`  
  Final Part B table including:
  - Raw revenue  
  - Adjusted revenue (Model 1 and Model 2)

- `outputs/financial_table_final.parquet`

---

### Figures

Plots are saved to:

```
outputs/figures/
```

This folder is tracked in Git.  
All other contents in `outputs/` are ignored.

---

## Methodology Overview

### Part A — Entity Resolution

- Text standardization for names and addresses
- **Blocking strategy:**
  - Pass 1: `(state, zip5)`
  - Pass 2 (fallback): `(state, city, zip3)` with Top-K pruning
- Token-based fuzzy similarity scoring
- Confidence labeling:
  - `match`
  - `possible`
  - `no_match`
  - `unmatched`
- Match provenance stored as `match_source`

---

### Part B — Revenue Adjustment

- **Model 1:** Constant multiplier (baseline card share assumption)
- **Model 2:** Segmented multiplier by `(business_entity_id × sqft_bucket)`  
  - Includes shrinkage  
  - Applies bounds  
- Plausibility and stability checks
- Visual model comparisons

---

## Reproducibility

- Path configuration centralized in `src/config.py`
- Large operations use DuckDB (`read_parquet`, `COPY`) to avoid memory issues
- All outputs are reproducible by rerunning notebooks
- No manual post-processing steps required

