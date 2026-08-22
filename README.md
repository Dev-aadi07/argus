# ARGUS

**ARGUS** is a data intelligence pipeline built to ingest, validate, store, analyze, and eventually learn from structured data.

The project is being developed incrementally, with each phase adding another layer toward a production-oriented **Data Engineering → AI/ML** system.

> **Current Status: Phase 2 Complete ✅**

---

## What is ARGUS?

ARGUS is designed around a simple idea:

```text
Raw Data
   ↓
Ingestion
   ↓
Validation
   ↓
Storage
   ↓
Analysis
   ↓
Intelligence
   ↓
Prediction
```

The long-term goal is to evolve ARGUS from a reliable data pipeline into an intelligent system capable of answering:

* What is happening?
* What changed?
* What is unusual?
* Why did it happen?
* What is likely to happen next?
* Why does the system believe that?

---

# Current Capabilities

ARGUS currently supports:

* CSV data ingestion
* Automated data-quality validation
* Invalid-record detection
* Valid/invalid data separation
* PostgreSQL persistence
* Ingestion history tracking
* Idempotent ingestion
* SQL-based analytics
* Database indexing
* Python ↔ PostgreSQL integration through SQLAlchemy
* Automated testing with pytest

---

# Architecture

```text
                         ARGUS
                           │
                           ▼
                    ┌────────────┐
                    │  CSV DATA  │
                    └──────┬─────┘
                           │
                           ▼
                      INGESTION
                           │
                           ▼
                      VALIDATION
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
                  VALID         INVALID
                    │             │
                    ▼             ▼
              PostgreSQL      QUARANTINE
                    │
          ┌─────────┴──────────┐
          │                    │
          ▼                    ▼
   TRANSACTIONS          INGESTION LOGS
          │
          ▼
      SQL ANALYSIS
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
 REGION PRODUCT PAYMENT
```

---

# Phase 0 — Project Foundation ✅

Established the foundation required for the project:

* Python virtual environment
* Project structure
* Dependency management
* Environment configuration
* PostgreSQL connection
* SQLAlchemy database engine
* Git repository

---

# Phase 1 — Data Ingestion & Quality Engine ✅

Built the first functional ARGUS pipeline.

### Data ingestion

ARGUS can load structured CSV data into a Pandas DataFrame.

### Data validation

The validation layer currently detects:

* Missing values
* Duplicate order IDs
* Negative quantities
* Negative prices
* Invalid dates

### Data separation

Records are separated into:

```text
Valid Data
    +
Invalid Data
```

Invalid records are prevented from entering the main database.

### Testing

The validation pipeline is covered with automated tests using `pytest`.

---

# Phase 2 — PostgreSQL Data Layer ✅

Phase 2 transformed ARGUS from a file-processing script into a persistent data pipeline.

## Database

ARGUS currently uses PostgreSQL with two core tables.

### `transactions`

Stores validated transaction records.

| Column           | Purpose                       |
| ---------------- | ----------------------------- |
| `order_id`       | Unique transaction identifier |
| `customer_id`    | Customer identifier           |
| `product_id`     | Product identifier            |
| `order_date`     | Transaction date              |
| `quantity`       | Units purchased               |
| `unit_price`     | Price per unit                |
| `discount`       | Applied discount              |
| `region`         | Customer/transaction region   |
| `payment_method` | Payment method                |

`order_id` acts as the primary key.

### `ingestion_logs`

Stores metadata about every ingestion.

Tracks:

* Source
* Ingestion timestamp
* Rows received
* Columns received
* Valid records
* Invalid records
* Data-quality score

This allows ARGUS to maintain a history of what happened during every ingestion.

---

# Data Quality Example

For the current sample dataset:

```text
Records received : 15
Valid records    : 10
Invalid records  : 5
Columns          : 9
Quality score    : 66.67%
```

The invalid records are identified before database insertion.

---

# Idempotent Ingestion

ARGUS uses PostgreSQL conflict handling to prevent duplicate transactions.

The transaction identifier is protected by the primary key:

```text
order_id
```

Repeated execution of:

```bash
python main.py
```

does not create duplicate transactions.

Instead, already-existing records are ignored.

This makes the ingestion pipeline **idempotent**.

---

# Analytics

ARGUS can now query PostgreSQL and generate analytical summaries.

## Overall Summary

```text
Total Transactions
Total Units
Total Revenue
```

## Regional Analysis

```text
Region
Transaction Count
Total Units
Total Revenue
```

## Product Analysis

```text
Product
Units Sold
```

## Payment Analysis

```text
Payment Method
Revenue
```

The SQL results are loaded back into Pandas for further analysis.

---

# Database Performance

Indexes have been added for commonly queried fields:

```text
transactions
│
├── PRIMARY KEY → order_id
├── INDEX       → region
├── INDEX       → order_date
└── INDEX       → product_id
```

ARGUS also uses PostgreSQL's `EXPLAIN ANALYZE` to inspect query execution plans.

The goal is to make the database layer capable of scaling beyond the current sample dataset.

---

# Project Structure

```text
argus/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── quarantine/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   │
│   ├── processing/
│   │
│   ├── analysis/
│   │
│   └── utils/
│
├── tests/
│
├── config/
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

# Tech Stack

### Core

* Python
* Pandas
* NumPy

### Database

* PostgreSQL
* SQLAlchemy
* psycopg2

### Testing

* pytest

### Development

* Git
* GitHub
* VS Code

---

# Running ARGUS

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd argus
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file containing the PostgreSQL configuration required by the project.

**Never commit `.env` or database credentials to GitHub.**

## 5. Run the complete pipeline

```bash
python main.py
```

## 6. Run analytics

```bash
python -m src.analysis.analytics
```

## 7. Run tests

```bash
pytest
```

---

# Development Roadmap

ARGUS is being developed in phases.

```text
Phase 0
Project Foundation
       ↓
Phase 1
Data Ingestion & Quality
       ↓
Phase 2
PostgreSQL + Analytics
       ↓
Phase 3
Advanced Data Processing
       ↓
Phase 4
Statistical Intelligence
       ↓
Phase 5
Anomaly Detection
       ↓
Phase 6
Forecasting
       ↓
Phase 7
Explainable AI
       ↓
Phase 8
API + Interface
       ↓
Phase 9
Docker + Production
       ↓
Phase 10
Streaming / ARGUS LIVE
```

---

# Future Direction

The next stages of ARGUS will focus on turning stored data into intelligence.

### Phase 3 — Advanced Data Processing

* Data transformations
* Feature engineering
* Reusable processing pipelines
* More robust data handling

### Phase 4 — Statistical Intelligence

* Trend analysis
* Correlation analysis
* Distribution analysis
* Business metrics

### Phase 5 — Anomaly Detection

ARGUS will learn to identify unusual patterns automatically.

### Phase 6 — Forecasting

ARGUS will use historical data to predict future behavior.

### Phase 7 — Explainability

The system will provide explanations alongside predictions.

### Phase 8 — API & Interface

Expose ARGUS through an API and user-facing interface.

### Phase 9 — Production

* Docker
* Deployment
* Monitoring
* Logging
* Configuration management

### Phase 10 — ARGUS LIVE

Move from batch CSV processing toward real-time/streaming data using technologies such as:

* Kafka
* Spark
* Streaming pipelines

---

# Engineering Principles

ARGUS is being built around a few core principles:

**Data quality first**

Bad data should be detected before it reaches downstream systems.

**Separation of concerns**

Ingestion, validation, storage, and analysis remain separate components.

**Database integrity**

Constraints and keys are used to protect stored data.

**Idempotency**

Repeated ingestion should not create duplicate records.

**Observability**

ARGUS records ingestion metadata so pipeline behavior can be inspected later.

**Scalability**

The architecture is being designed with larger datasets and production workloads in mind.

**Explainability**

Future AI predictions should be understandable rather than treated as black-box outputs.

---

# Project Vision

ARGUS started as a simple Python data-validation pipeline.

It is now evolving into a complete data intelligence system.

The ultimate objective is:

```text
              RAW DATA
                  │
                  ▼
             DATA QUALITY
                  │
                  ▼
              DATA LAKE
                  │
                  ▼
             ANALYTICS
                  │
                  ▼
          MACHINE LEARNING
                  │
                  ▼
            PREDICTIONS
                  │
                  ▼
             EXPLANATIONS
```

**ARGUS — From raw data to actionable intelligence.**
