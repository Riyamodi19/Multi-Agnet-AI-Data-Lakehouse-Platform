# Phase 3: Data Lakehouse Implementation (Bronze & Silver Layers)

## Overview
This module implements **Phase 3 — Data Lakehouse Implementation** using **MinIO S3 Object Storage** architecture and **Apache Arrow / PyArrow / Pandas** columnar Parquet formats.

## Lakehouse Layer Architecture
```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                               MINIO OBJECT STORAGE                                            │
│                                                                                               │
│ Bronze Parquet Files: 549 Raw JSON Scraped Documents                                          │
│ Silver Parquet Files: 38,407 Cleaned, Extracted & Deduplicated Payment Entities              │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Bronze Parquet Layer (`lakehouse/warehouse/storage/bronze/`)
- Contains all **549 raw scraped JSON files** converted into columnar Bronze Parquet (`bronze_raw_payments.parquet`).
- Preserves complete raw unparsed HTML, full plain text body, and original metadata for auditability.

### 2. Silver Parquet Layer (`lakehouse/warehouse/storage/silver/`)
- Contains **38,407 extracted, cleaned, and deduplicated payment method entities** saved as Silver Parquet (`silver_cleaned_payments.parquet`).
- **Cleaned Fields**:
  - `site_name`: Normalized platform name (22Bet, Melbet, 10Cric, 1xBet)
  - `payment_method_name`: Extracted payment title (PhonePe, PayTM, Google Pay, UPI Intent, Bitcoin, Tether, etc.)
  - `category`: Standardized category (Cryptocurrency, E-Wallet, Bank Transfer, Payment Cards, Mobile Payments)
  - `data_agent`: Payment aggregator agent (`bt3`, `accentpay`, `cryptocurrencies2`, `odeonpay`, `pacopay`)
  - `data_method_code`: Backend method string
  - `upi_id`, `bank_account`, `ifsc_code`: Cleaned payment account identifiers
  - `data_quality_score`: 100% Quality Score index

## Data Cleaning & Transformation Pipeline
1. **Raw Schema Ingestion**: Validated document integrity across 549 JSON payloads.
2. **HTML DOM Element Parsing**: Parsed dynamic `<div class="payment-cell">` nodes from 200KB-900KB raw HTML files.
3. **UTF-8 Repair & Formatting**: Removed HTML tags, encoding artifacts, and leading/trailing whitespace.
4. **Category Standardisation**: Mapped raw site categories into 7 standardized business payment categories.
5. **Regex Extraction & Imputation**: Extracted UPI IDs and bank account details; imputed optional missing values with `'N/A'`.
6. **Deduplication**: Removed duplicate DOM cards per site.

## Visualizations & PDF Report Generation
All data cleaning results, audit metrics, 5 charts, and viva presentation guidelines have been compiled into a professional PDF report saved in the project description directory:
`project description/Phase3_Data_Lakehouse_Cleaning_and_Visualization_Report.pdf`

## Execution Command
```bash
# Run Lakehouse Bronze & Silver ETL, generate charts, and create PDF report
python build_phase3_lakehouse_and_report.py
```
