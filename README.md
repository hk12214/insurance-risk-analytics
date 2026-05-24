# ACIS End-to-End Insurance Risk Analytics

Predictive pricing and marketing risk modeling framework for AlphaCare Insurance Solutions (ACIS), optimizing auto-insurance operations in South Africa using historical claims data (Feb 2014 – Aug 2015).

## Project Architecture

```text
insurance-risk-analytics/
├── .github/workflows/ci.yml   # GitHub Actions Continuous Integration
├── data/                      # Local data storage directory (DVC tracked)
├── notebooks/                 # Exploratory, testing, and training environments
│   ├── 01_eda.ipynb
│   ├── 02_hypothesis_testing.ipynb
│   └── 03_modeling.ipynb
├── src/                       # Production-grade production source modules
│   ├── data_loader.py
│   ├── eda_utils.py
│   ├── hypothesis_tests.py
│   └── modeling.py
├── tests/                     # Unit testing suites
├── requirements.txt           # Base environment declarations
└── README.md
## Quick Start & Setup
 1. Clone the repository and build a virtual workspace:
```bash
   git clone https://github.com/hk12214/insurance-risk-analytics.git
   cd insurance-risk-analytics
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
```
2. Validation Framework:
The continuous integration pipeline automatically enforces style rules and tests using flake8 and pytest on every remote push.
## Data Version Control (DVC) & Pipeline Reproducibility

This project utilizes Data Version Control (DVC) alongside Git to build a fully reproducible, secure, and auditable data tracking environment. Raw data and processed artifacts are stored outside of the source control history to optimize performance and adhere to compliance regulations in financial environments.

### The Pipeline Architecture

The raw state and processed states are split into decoupled tracking layers:
* `data/insurance_data.csv.dvc`: The small, text-based pointer hash configuration managed by Git.
* `../dvc_remote_storage`: The external local remote file vault managing the physical `.csv` datasets via md5 cryptographic signatures.

### How to Reproduce the Data Environment

To perfectly replicate the data environment and check out a specific version snapshot of the insurance data files on your machine, execute the following commands in sequence:

```bash
# 1. Clone the active project repository footprint
git clone [https://github.com/hk12214/insurance-risk-analytics.git](https://github.com/hk12214/insurance-risk-analytics.git)
cd insurance-risk-analytics

# 2. Check out the specific branch or tag you wish to inspect
# For Raw Baseline Data: git checkout v1-raw
# For Cleaned Modeling Data: git checkout v2-cleaned
git checkout task-2

# 3. Pull down the tracked data files matching that specific point in time
dvc pull