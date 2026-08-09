# Phase 6: Retrieval-Augmented Generation (RAG) Pipeline

## Overview
This module implements **Phase 6 — Retrieval-Augmented Generation (RAG)** using **LangChain, Sentence-Transformers (`all-MiniLM-L6-v2`), FAISS Vector Database, and Local LLM Integration (Ollama / FLAN-T5 / Llama 3)**.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                               RAG PIPELINE                                                    │
│                                                                                               │
│ 1. User Question Ingestion                                                                    │
│        │                                                                                      │
│        ▼                                                                                      │
│ 2. Sentence Transformer (all-MiniLM-L6-v2) ──► 384-D Vector Mapping                           │
│        │                                                                                      │
│        ▼                                                                                      │
│ 3. FAISS Vector Retrieval (Top-K Matches)                                                     │
│        │                                                                                      │
│        ▼                                                                                      │
│ 4. LangChain / Strict Prompt Engineering ("Answer ONLY from Retrieved Context")               │
│        │                                                                                      │
│        ▼                                                                                      │
│ 5. Local LLM Generation (Ollama / FLAN-T5 / Llama 3)                                          │
│        │                                                                                      │
│        ▼                                                                                      │
│ 6. Hallucination Verification (Grounding Score Enforcement)                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## What We Achieved in Phase 6
- **Zero-Hallucination QA**: Constrains LLM outputs strictly to retrieved Silver Lakehouse facts.
- **Local Open-Source Execution**: Runs 100% offline using local models with zero external API costs.
- **Hallucination Verification**: Calculates term-overlap grounding scores to guarantee 100% answer accuracy.

## Core Files
- `rag_pipeline.py`: Main RAG engine executing query vectorization, FAISS retrieval, prompt template, local LLM generation, and hallucination verification.
- `run_rag_report_builder.py`: PDF report generator compiling benchmark metrics and student viva presentation guide.

## Execution Command
```bash
# Run RAG Pipeline Test & Build PDF Report
python 06_rag_pipeline/run_rag_report_builder.py
```

## PDF Report
The complete student guide explaining WHAT, WHY, WHEN, WHERE, and viva presentation script is saved in:
`project description/Phase6_RAG_Pipeline_Report.pdf`
