import os
import json
import time
import pandas as pd
import numpy as np

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = r"d:\final_end_game"
AGENT_DIR = os.path.join(BASE_DIR, "07_multi_agent_framework")
PROJECT_DESC_DIR = os.path.join(BASE_DIR, "project description")

os.makedirs(AGENT_DIR, exist_ok=True)
os.makedirs(PROJECT_DESC_DIR, exist_ok=True)

print("Starting Phase 7 Multi-Agent Report Generation...")

pdf_path1 = os.path.join(PROJECT_DESC_DIR, "Phase7_MultiAgent_AI_Framework_Report.pdf")
pdf_path2 = os.path.join(PROJECT_DESC_DIR, "MultiAgent_AI_Phase7_Complete_Guide.pdf")

doc = SimpleDocTemplate(pdf_path1, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
styles = getSampleStyleSheet()

primary_color = colors.HexColor("#1A365D")
secondary_color = colors.HexColor("#2B6CB0")
accent_color = colors.HexColor("#C53030")
dark_text = colors.HexColor("#2D3748")
bg_light = colors.HexColor("#F7FAFC")

title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=primary_color, alignment=1, spaceAfter=4)
sub_style = ParagraphStyle('DocSub', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=14, textColor=secondary_color, alignment=1, spaceAfter=10)
h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=primary_color, spaceBefore=12, spaceAfter=6, keepWithNext=True)
h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=secondary_color, spaceBefore=8, spaceAfter=4, keepWithNext=True)
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=dark_text, spaceAfter=5)
bullet_style = ParagraphStyle('Bullet', parent=body_style, leftIndent=12, bulletIndent=4, spaceAfter=3)

story = []

# Title Banner
story.append(Paragraph("Phase 7 — Multi-Agent AI Framework & Agentic Orchestrator", title_style))
story.append(Paragraph("<b>Complete Student Guide: Architecture, Tools, Agent Capabilities & Purpose</b><br/><i>Written in Simple Language for Academic & Viva Presentation</i>", sub_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

# Executive Summary
story.append(Paragraph("1. Executive Summary & Purpose of Phase 7", h1_style))
exec_text = (
    "In <b>Phase 7: Multi-Agent AI Framework</b>, we integrated all previous components (Scraping, Kafka Ingestion, MinIO Lakehouse, Scikit-Learn ML Models, FAISS Vector Search, and LangChain RAG) into a single <b>Autonomous Agentic AI Framework</b>.<br/><br/>"
    "<b>What is an Agentic AI Orchestrator?</b><br/>"
    "Instead of forcing a human to run separate Python scripts manually, an Agentic Orchestrator acts as a smart manager. "
    "When given a high-level goal (like <i>'Scrape Melbet, clean data, run anomaly checks, and produce a report'</i>), "
    "the Master Orchestrator automatically assigns tasks to specialized sub-agents, tracks progress using unique correlation IDs, and executes the entire pipeline end-to-end without human intervention."
)
story.append(Paragraph(exec_text, body_style))
story.append(Spacer(1, 6))

# Specialized Sub-Agents & Tool Architecture Table
story.append(Paragraph("2. Specialized Sub-Agents & Available Tools", h1_style))

agent_table_data = [
    [Paragraph("<b>Sub-Agent Name</b>", body_style), Paragraph("<b>Equipped Tool</b>", body_style), Paragraph("<b>Role & Operational Description</b>", body_style)],
    [Paragraph("<b>Scraper Manager Agent</b>", body_style), Paragraph("<code>Scraper Tool</code>", body_style), Paragraph("Controls Scrapy and Playwright crawlers to automatically fetch new payment web pages.", body_style)],
    [Paragraph("<b>Data Validator & ETL Agent</b>", body_style), Paragraph("<code>Spark / Lakehouse ETL Tool</code>", body_style), Paragraph("Ingests raw JSON payloads into Bronze Parquet & cleans extracted payment records into Silver Parquet.", body_style)],
    [Paragraph("<b>Anomaly Detector Agent</b>", body_style), Paragraph("<code>ML Analysis Tool</code>", body_style), Paragraph("Runs Random Forest, Isolation Forest, and K-Means models to detect suspicious payment routes.", body_style)],
    [Paragraph("<b>RAG Query Handler Agent</b>", body_style), Paragraph("<code>Vector Search & RAG Tool</code>", body_style), Paragraph("Queries the 384-D FAISS vector index and local LLM to answer natural language user queries.", body_style)],
    [Paragraph("<b>Report Generator Agent</b>", body_style), Paragraph("<code>Report Generator Tool</code>", body_style), Paragraph("Compiles PDF summary reports and persists audit logs.", body_style)],
    [Paragraph("<b>Master Agentic Orchestrator</b>", body_style), Paragraph("<code>Orchestrator Control</code>", body_style), Paragraph("Central controller that registers agents, routes inter-agent messages, and triggers automated workflows.", body_style)]
]

t_agent = Table(agent_table_data, colWidths=[125, 110, 255])
t_agent.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), secondary_color),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
    ('PADDING', (0,0), (-1,-1), 4),
]))
story.append(t_agent)
story.append(Spacer(1, 8))

# Agent Capabilities Checklist
story.append(Paragraph("3. Agent Capabilities Checklist", h1_style))
story.append(Paragraph("The Agentic Orchestrator possesses 9 autonomous operational capabilities:", body_style))

caps = [
    "<b>✓ Scrape New Betting Site:</b> Automatically triggers scraping spiders for new betting platforms.",
    "<b>✓ Process New Data:</b> Ingests raw JSON into Bronze & Silver Lakehouse storage.",
    "<b>✓ Detect Fraud & Anomalies:</b> Evaluates transaction feature vectors using Isolation Forest.",
    "<b>✓ Compare Betting Sites:</b> Computes cross-site payment category distributions.",
    "<b>✓ Search Similar Payment Pages:</b> Uses FAISS 384-D vector search to locate similar payment options.",
    "<b>✓ Generate Investigation Reports:</b> Produces structured PDF reports automatically.",
    "<b>✓ Answer Natural Language Questions:</b> Invokes the Phase 6 RAG pipeline for zero-hallucination QA.",
    "<b>✓ Explain ML Predictions:</b> Details feature importance Gini weights.",
    "<b>✓ Trigger Entire Pipeline Automatically:</b> Executes end-to-end workflows from a single user intent."
]

for cap in caps:
    story.append(Paragraph(cap, bullet_style))

story.append(Spacer(1, 8))

# How This Helps & Purpose
story.append(Paragraph("4. How Is This Helpful & What Is Its Purpose?", h1_style))
help_text = (
    "<b>How This Is Helpful:</b><br/>"
    "• <b>1. Zero Manual Coordination:</b> Eliminates the need for humans to run 7 different scripts manually.<br/>"
    "• <b>2. Event-Driven Automation:</b> If new data is scraped, the Scraper Agent automatically notifies the ETL Agent, which in turn notifies the Anomaly Detector Agent.<br/>"
    "• <b>3. Scalability:</b> New sub-agents (e.g. Graph Database Agent or Blockchain Agent) can be added without rewriting the platform.<br/><br/>"
    "<b>Purpose of Making It:</b><br/>"
    "In modern enterprise AI systems, data pipelines are complex. An Agentic AI Framework transforms isolated tools into a **cohesive, self-orchestrating intelligence platform** capable of autonomous decision-making."
)
story.append(Paragraph(help_text, body_style))
story.append(Spacer(1, 8))

# Presentation Viva Script for Ma'am
story.append(Paragraph("5. Presentation Script & Viva Talking Points for Ma'am", h1_style))
story.append(Paragraph("Use these exact line-by-line talking points when presenting Phase 7 to your professor:", body_style))

script_agent_items = [
    "<b>Introduction:</b> 'Respected Ma'am, in Phase 7 we integrated all our system layers into a Multi-Agent AI Framework managed by an Agentic Orchestrator.'",
    "<b>Role of Orchestrator:</b> 'Rather than running separate scripts manually, the Master Orchestrator receives high-level user goals and delegates sub-tasks to specialized agents like the Scraper Manager, Data Validator, Anomaly Detector, and RAG Handler.'",
    "<b>Inter-Agent Messaging:</b> 'Sub-agents communicate using structured JSON messages with unique correlation IDs for complete execution tracking.'",
    "<b>Automated Execution:</b> 'We successfully tested automated full-pipeline execution, where a single command automatically scraped data, ran Spark/Lakehouse ETL, performed Isolation Forest anomaly detection, queried FAISS vector index, and built PDF reports.'",
    "<b>Outcome:</b> 'This completes our student platform, demonstrating end-to-end Agentic AI orchestration across Big Data and Machine Learning components.'"
]

for item in script_agent_items:
    story.append(Paragraph(f"• {item}", bullet_style))

story.append(Spacer(1, 12))
story.append(HRFlowable(width="100%", thickness=1, color=secondary_color, spaceAfter=6))
story.append(Paragraph("<i>Report generated automatically by Phase 7 Agentic AI Framework Engine | Student Open-Source Edition</i>", ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, alignment=1, textColor=colors.gray)))

doc.build(story)

doc2 = SimpleDocTemplate(pdf_path2, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
doc2.build(story)

print(f"Phase 7 PDF 1 created at: {pdf_path1}")
print(f"Phase 7 PDF 2 created at: {pdf_path2}")

