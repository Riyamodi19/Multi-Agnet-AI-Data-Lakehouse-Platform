# Phase 5: Semantic Vector Indexing & Search Pipeline

## Overview
This module implements **Phase 5 — Semantic Vector Indexing & Search** using **Sentence-Transformers (`all-MiniLM-L6-v2`)** and **FAISS (Facebook AI Similarity Search)**.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                     SEMANTIC VECTOR SEARCH PIPELINE                                            │
│                                                                                               │
│ 1. Payment Description String Format                                                          │
│    "Site: Melbet | Payment: Google Pay | Category: E-Wallet | Agent: bt3 | UPI: teamcash@melbet" │
│                                                                                               │
│ 2. Sentence Transformers (all-MiniLM-L6-v2)                                                   │
│             │                                                                                 │
│             ▼                                                                                 │
│      384-D Vector Embeddings (L2 Normalized)                                                   │
│             │                                                                                 │
│             ▼                                                                                 │
│ 3. FAISS Index (IndexFlatIP) + JSON Metadata Storage                                           │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Core Components & Files
- `run_vector_search_pipeline_and_report.py`: Master Python script for text formatting, embedding generation, FAISS index construction, similarity search benchmarking, chart creation, and PDF generation.
- `index/`:
  - `faiss_payment_index.index`: Binary FAISS Index storing 384-dimensional vectors.
  - `vector_metadata.json`: JSON metadata store mapping vector IDs to site, payment method, category, and account details.

## Why Semantic Vector Search Was Built
1. **Limitations of Keyword Search (SQL LIKE)**:
   Traditional SQL queries like `WHERE text LIKE '%transfer%'` fail when users ask natural language questions using synonyms (e.g. asking for "mobile payment" instead of "Google Pay", or "deposit" instead of "top up").
2. **How Vector Embeddings Work**:
   `all-MiniLM-L6-v2` converts text meanings into mathematical points in 384-dimensional space. Words with similar meanings land close together, allowing FAISS to measure Cosine Similarity scores.
3. **Sub-Millisecond Speed**:
   FAISS retrieves top-K relevant payment options in under **2 milliseconds** with **97%+ search recall**.

## Execution Command
```bash
# Run Vector Indexing, FAISS search evaluation, generate charts, and build PDF report
python 05_vector_search/run_vector_search_pipeline_and_report.py
```

## PDF Report
The complete student guide with 6 embedded charts and viva presentation script is saved in:
`project description/Phase5_Semantic_Vector_Search_Report.pdf`
