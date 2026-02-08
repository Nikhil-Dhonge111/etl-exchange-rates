# 🚀 Exchange Rates ETL Pipeline (Python + CI)

## 📌 Project Overview

This project is a **simple but production-oriented ETL pipeline** built using free tools to gain hands-on confidence in data engineering fundamentals.

The pipeline:
- **Extracts** exchange rate data from a public API
- **Transforms** it using Python & Pandas
- **Loads** it into a SQL database (SQLite)
- Implements **incremental loading**
- Applies **data quality checks**
- Is protected by **unit tests and CI using GitHub Actions**

This project focuses on **engineering decisions and problem-solving**, not just writing scripts.

---

## 🧠 Motivation

The goal of this project was to move from:
> “I can write Python scripts”  
to  
> “I can design, test, and validate a data pipeline like a data engineer”

While building this project, I intentionally faced and solved real-world issues such as:
- Broken imports
- CI failures
- Missing dependencies
- Incremental load bugs
- API mocking challenges

---

## 🏗️ High-Level Architecture
```
Public Exchange Rate API
    ⬇️
Extract (requests)
    ⬇️
Transform (pandas + validations)
    ⬇️
Load (SQLite)
    ⬇️
Unit Tests (pytest)
    ⬇️
CI Pipeline (GitHub Actions)
```

---

## 🔄 ETL Workflow

### 1️⃣ Extract
- Fetches daily exchange rates from a public API
- Uses timeouts and error handling
- External API calls are **mocked in tests**

### 2️⃣ Transform
- Converts JSON response into a tabular structure
- Adds metadata columns:
  - `base_currency`
  - `date`
  - `ingested_at`
- Applies **data quality rules**:
  - No NULL values
  - No zero or negative exchange rates

### 3️⃣ Load
- Loads data into a SQL table
- Implements **incremental loading**
- Skips ingestion if data for the same date already exists
- Prevents duplicate records

---

## 🧪 Testing Strategy

### Unit Tests
- `test_transform.py` validates transformation logic
- `test_extract.py` mocks API responses (no real API calls)
- Ensures data quality rules are enforced

### Why Mocking?
- CI environments must be deterministic
- External APIs can fail or rate-limit
- Real production pipelines never depend on live APIs during tests

---

## ⚙️ CI/CD with GitHub Actions

Every push or pull request:
- Installs dependencies from scratch
- Runs all unit tests
- Fails the build if any test fails

Branch protection ensures:
- ❌ No direct pushes to `main`
- ✅ Only tested pull requests can be merged

---

## 🧩 Problems Faced & How They Were Solved

### ❌ Problem 1: SQL SyntaxError in Python
**Issue**
```python
SELECT max(date) FROM exchange_rates
```

Learning
SQL cannot be written directly in Python code

Solution
```
cursor.execute("SELECT MAX(date) FROM exchange_rates")
```

### ❌ Problem 2: Incremental Load Always Skipped
**Issue**
- Table was being dropped on every run
- Incremental logic never worked

Learning
- Incremental pipelines must preserve state

Solution
- Removed DROP TABLE
- Used MAX(date) to detect new data

### ❌ Problem 3: CI Failed but Local Tests Passed  
**Issue**
- fixture 'mocker' not found

Root Cause
- pytest-mock dependency missing in CI

Learning
- CI runs in a clean environment
- If it’s not in requirements.txt, it doesn’t exist

Solution
- Added pytest-mock to requirements.txt

### ❌ Problem 4: ImportError While Running Tests  
**Issue**
- Python imported an installed etl package instead of project code

Learning
- File naming conflicts can silently break imports

Solution
- Renamed modules
- Used explicit imports and clean project structure

### ❌ Problem 5: How to Validate CI Configuration  
Learning
- CI cannot be fully tested locally
  
Validation approach:
- Run tests locally
- Push code
- Debug using GitHub Actions logs

Outcome
- CI failures became easier to debug than local ones

## 🧠 Key Engineering Concepts Demonstrated
- Incremental data loading
- Data quality validation
- API mocking
- Unit testing
- CI/CD pipelines
- Branch protection rules
- Reproducible environments

## 📂 Project Structure
```
etl-exchange-rates/
│
├── ETL_pipeline.py
├── requirements.txt
├── tests/
│   ├── test_extract.py
│   └── test_transform.py
│
└── .github/
    └── workflows/
        └── ci.yml
```        
### ▶️ How to Run Locally
```python
pip install -r requirements.txt
python ETL_pipeline.py
pytest -v
```
### 📦 Data Persistence & Consumption
Why Data Is Not Visible After Scheduled Runs
- This pipeline is executed using GitHub Actions, which runs jobs on ephemeral runners.

Key behavior:
- Each run executes on a fresh virtual machine
- Any locally created files (SQLite DB, CSVs, raw data) exist only during the run
- After the job finishes, the runner is destroyed
- Therefore, the SQLite database is not persisted automatically
- This behavior is expected and mirrors real production CI environments.

How Data Is Persisted for Validation
- To inspect and validate the generated data during development, the SQLite database is uploaded as a GitHub Actions artifact.

This allows:
- Downloading the database after each run
- Verifying tables and records locally
- Debugging incremental loads and data quality issues

This approach is used only for learning and validation.
In production systems, data would be written to an external persistent store such as:
- PostgreSQL / Azure SQL
- Cloud object storage (Azure Blob / S3)

How the Data Can Be Used
- Once persisted in an external database, the processed exchange rate data can be consumed by downstream applications, such as:
- Analytical dashboards
    - Streamlit dashboards
    - Power BI / Tableau
    - Metabase
- APIs
    - Exposing exchange rates via REST endpoints
    - Powering internal or external applications
- Reporting systems
    - Scheduled market insight reports
    - Trend analysis and historical comparisons

This separation of data ingestion and data consumption reflects standard data engineering architecture.
### 📈 Future Enhancements
- Replace SQLite with PostgreSQL / Azure SQL
- Add structured logging
- Add retry and alerting logic
- Orchestrate with Airflow or Azure Data Factory
- Containerize with Docker
