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

Public Exchange Rate API
|
v
Extract (requests)
|
v
Transform (pandas + validations)
|
v
Load (SQLite)
|
v
Unit Tests (pytest)
|
v
CI Pipeline (GitHub Actions)


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
cursor.execute("SELECT MAX(date) FROM exchange_rates")

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
- 
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
        
### ▶️ How to Run Locally
```python
pip install -r requirements.txt
python ETL_pipeline.py
pytest -v
```

### 📈 Future Enhancements
- Replace SQLite with PostgreSQL / Azure SQL
- Add structured logging
- Add retry and alerting logic
- Orchestrate with Airflow or Azure Data Factory
- Containerize with Docker
