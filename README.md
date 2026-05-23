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