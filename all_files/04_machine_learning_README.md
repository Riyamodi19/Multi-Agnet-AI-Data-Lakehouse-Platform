# Phase 4: Machine Learning & Analytics Pipeline

## Overview
This module implements **Phase 4 — Machine Learning & Analytics** using **scikit-learn, PyArrow, Pandas, and Matplotlib**. The pipeline extracts engineered features from the Silver Data Lakehouse dataset (38,407 records) and trains 3 machine learning models.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                          MACHINE LEARNING PIPELINE                                             │
│                                                                                               │
│ Feature Engineering                                                                          │
│ • upi_present (Binary: 0/1)                                                                  │
│ • bank_account_present (Binary: 0/1)                                                         │
│ • crypto_present (Binary: 0/1)                                                               │
│ • payment_type / target_category (Class: 0, 1, 2, 3)                                         │
│ • amount (Numeric Limit/Transaction Amount)                                                  │
│ • site_name (One-Hot Encoded: Melbet, 22Bet, 10Cric, 1xBet)                                 │
│                                                                                               │
│ Models & Evaluation                                                                           │
│ • Random Forest Classifier (Accuracy: 100.0%, Precision: 1.0000, Recall: 1.0000, F1: 1.0000)  │
│ • Isolation Forest Anomaly Detection (Inliers: 36,528 [95.1%], Outliers: 1,879 [4.9%])       │
│ • K-Means Clustering (K=4, Silhouette Score: 0.7678)                                          │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Directory Structure
- `run_ml_pipeline_and_generate_report.py`: Master Python script for feature engineering, model training, evaluation, chart creation, and PDF generation.
- `models/`:
  - `random_forest_model.pkl` (Trained Random Forest Classifier)
  - `isolation_forest_model.pkl` (Trained Isolation Forest Anomaly Detector)
  - `kmeans_clustering_model.pkl` (Trained K-Means Clustering Model)
  - `feature_scaler.pkl` (StandardScaler feature transformer)
- `ml_metrics_summary.json`: JSON output containing evaluation metrics.

## Model Evaluation Metrics

### 1. Random Forest Classifier (Supervised Classification)
- **Accuracy**: 100.00% (`1.0000`)
- **Precision**: 100.00% (`1.0000`)
- **Recall**: 100.00% (`1.0000`)
- **F1 Score**: 100.00% (`1.0000`)

### 2. Isolation Forest (Unsupervised Anomaly Detection)
- **Contamination Rate**: 5.0%
- **Normal Transactions (Inliers)**: 36,528 records (95.1%)
- **Anomalous Transactions (Outliers)**: 1,879 records (4.9%)

### 3. K-Means Clustering (Unsupervised Segmentation)
- **Optimal Clusters (K)**: 4 Clusters
- **Silhouette Score**: **0.7678**

## PDF Report & Documentation
The complete presentation report with 6 embedded charts and viva guide is saved in:
`project description/Phase4_Machine_Learning_and_Analytics_Report.pdf`
