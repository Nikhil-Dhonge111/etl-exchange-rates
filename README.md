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

