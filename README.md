# ARGUS

ARGUS is a data intelligence system designed to ingest, validate, store, analyze, and eventually learn from continuously changing datasets.

The project is being built incrementally as a real data/AI engineering system.

---

## Current Status

### Phase 2 — PostgreSQL Data Layer ✅

ARGUS currently supports:

- CSV data ingestion
- Data-quality validation
- Valid/invalid record separation
- PostgreSQL persistence
- Ingestion history logging
- Idempotent database ingestion
- SQL-based analytics
- Database indexes
- Automated pipeline tests

---

## Architecture

```text
                         ARGUS
                           │
                           ▼
                    ┌────────────┐
                    │ CSV SOURCE │
                    └──────┬─────┘
                           │
                           ▼
                     INGESTION
                           │
                           ▼
                     VALIDATION
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                  VALID         INVALID
                    │             │
                    ▼             ▼
              PostgreSQL      Quarantine
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   transactions         ingestion_logs
          │
          ▼
     SQL ANALYTICS
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
 REGION PRODUCT PAYMENT