# Phase 2: Real-Time Streaming Ingestion (Kafka)

## Overview
This module handles real-time data streaming ingestion using **Apache Kafka**. Scraped raw JSON records are streamed into Kafka topics, validated, and processed before landing in the Bronze Lakehouse layer.

## Architecture & Components
- **`kafka_producer.py` / `load_json_to_kafka.py`**:
  Reads scraped JSON payloads and publishes streaming events to Kafka topics (`payment-methods-raw`, `transactions-clean`).
- **`kafka_consumer.py`**:
  Subscribes to raw Kafka topics, performs real-time schema validation, handles consumer partition rebalancing, exports Prometheus metrics (`http://localhost:8001/metrics`), and writes validated events into date-partitioned Bronze Lakehouse storage.
- **Dead-Letter Queue (DLQ)**:
  Corrupted or invalid payloads (e.g. missing required fields or non-numeric amounts) are automatically routed to `dead-letter-queue` for fault isolation without blocking stream processing.

## Kafka Topics Configured
1. `payment-methods-raw`: Unprocessed payment method scraped payloads.
2. `transactions-clean`: Validated transaction records.
3. `dead-letter-queue` (DLQ): Poison pill and failed validation payloads.
4. `stream-retry`: Retried events.

## Execution Guide
```bash
# Start Kafka Producer to load JSON files to Kafka topics
python load_json_to_kafka.py

# Start Kafka Stream Consumer & Prometheus Metrics Exporter
python kafka_consumer.py
```
