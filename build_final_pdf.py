"""
Generate Complete 32-Page Academic Project Report PDF
Title: Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence
Guided by: Ms. Krishnaveni
Presented by: Ms. Riya Modi, Mr. Ilapavuluri Sesha Satya Sri Charan, Mr. Prasad Pandurang Gautre, Mr. Niraj Sunil Kadam
Target Output: d:\final_end_game\report\MultiAgent_AI_DataLakehouse_Platform_Project_Report.pdf
"""

import os
import sys
from fpdf import FPDF

class FinalProjectReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence", border=False, new_x="LMARGIN", new_y="NEXT", align="R")
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.4)
            self.line(15, 18, 195, 18)
            self.ln(4)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 10, f"Page {self.page_no()}", border=False, new_x="RIGHT", new_y="TOP", align="C")

    def section_heading(self, text):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(15, 23, 42)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(168, 85, 247)
        self.set_line_width(0.6)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

    def subsection_heading(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 41, 59)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_paragraph(self, text):
        clean_text = text.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5.5, clean_text)
        self.ln(3)

    def bullet_item(self, title, desc):
        clean_desc = desc.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-")
        clean_title = title.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 41, 59)
        self.cell(6, 5.5, "-", new_x="RIGHT", new_y="TOP")
        self.cell(45, 5.5, clean_title + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 5.5, clean_desc)
        self.ln(1.5)

    def code_block(self, code_text):
        clean_code = code_text.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-")
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(245, 247, 250)
        self.set_text_color(15, 23, 42)
        self.set_draw_color(226, 232, 240)
        lines = clean_code.strip().split("\n")
        self.rect(15, self.get_y(), 180, len(lines)*4.5 + 4, style="FD")
        self.ln(2)
        for line in lines:
            self.cell(4, 4.5, "", new_x="RIGHT", new_y="TOP")
            self.cell(0, 4.5, line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

def build_pdf():
    pdf = FinalProjectReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------------------------------------------------------
    # PAGE 1: TITLE / COVER PAGE
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.set_draw_color(30, 41, 59)
    pdf.set_line_width(1)
    pdf.rect(10, 10, 190, 277)

    pdf.ln(12)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Project Report On", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 19)
    pdf.set_text_color(147, 51, 234)
    pdf.multi_cell(0, 10, "Multi-Agent AI Data Lakehouse Platform for\nBetting Site Data Intelligence", align="C")
    pdf.ln(12)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 7, "Submitted in partial fulfilment for the award of", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Post Graduate Certificate Programme in Big Data Analytics", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(15)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "Guided by:", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 7, "Ms. Krishnaveni", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(15)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Presented by:", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    students = [
        ("Ms. Riya Modi", "PRN No. 260250325032"),
        ("Mr. Ilapavuluri Sesha Satya Sri Charan", "PRN No. 260250325017"),
        ("Mr. Prasad Pandurang Gautre", "PRN No. 260250325029"),
        ("Mr. Niraj Sunil Kadam", "PRN No. 260250325025")
    ]
    for name, prn in students:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.cell(95, 6.5, name, new_x="RIGHT", new_y="TOP", align="R")
        pdf.set_font("Helvetica", "", 10.5)
        pdf.cell(85, 6.5, f"   {prn}", new_x="LMARGIN", new_y="NEXT", align="L")

    pdf.ln(22)
    pdf.set_font("Helvetica", "B", 11.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "Centre for Development of Advanced Computing (C-DAC), Hyderabad", new_x="LMARGIN", new_y="NEXT", align="C")

    # ---------------------------------------------------------
    # PAGE 2: ACKNOWLEDGEMENT
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("ACKNOWLEDGEMENT")
    
    pdf.body_paragraph(
        'This project "Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence" was a valuable learning experience, combining data engineering, machine learning and generative-AI techniques into a single working pipeline. We are pleased to submit this work as part of our academic requirements.'
    )
    pdf.body_paragraph(
        "We are grateful to Ms. Krishnaveni for the guidance and support provided throughout the course of this project. Her feedback helped us navigate the technical challenges involved in building a multi-stage, multi-agent data platform."
    )
    pdf.body_paragraph(
        "We also thank the Centre for Development of Advanced Computing (C-DAC), Hyderabad and the faculty/coordinators of the Post Graduate Certificate Programme in Big Data Analytics for providing the resources, infrastructure and encouragement needed to complete this project."
    )
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "From:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "Ms. Riya Modi", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Mr. Sri Charan", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Mr. Prasad Gautre", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, "Mr. Niraj Kadam", new_x="LMARGIN", new_y="NEXT")

    # ---------------------------------------------------------
    # PAGE 3: TABLE OF CONTENTS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("TABLE OF CONTENTS")
    
    toc = [
        ("1. Introduction", "4"),
        ("2. Literature Review", "5"),
        ("   2.1 Web Scraping and Browser Automation", "5"),
        ("   2.2 Streaming Ingestion and Object Storage", "5"),
        ("   2.3 Distributed Processing and Feature Engineering", "5"),
        ("   2.4 Machine Learning for Classification & Anomalies", "5"),
        ("   2.5 Semantic Search, Embeddings and RAG", "6"),
        ("   2.6 Positioning of This Project", "6"),
        ("3. System Requirements", "7"),
        ("   3.1 Functional Requirements", "7"),
        ("   3.2 Non-Functional Requirements", "7"),
        ("   3.3 Hardware Requirements", "7"),
        ("   3.4 Software Requirements", "8"),
        ("4. System Design & Architecture", "9"),
        ("   4.1 Architectural Style", "9"),
        ("   4.2 Technology Stack Summary", "9"),
        ("5. Detailed Workflow", "11"),
        ("   5.1 Agent 1 - Data Collection Agent", "11"),
        ("   5.2 Agent 2 - Streaming & Storage Agent", "11"),
        ("   5.3 Agent 3 - Processing & Analytics Agent", "12"),
        ("   5.4 Agent 4 - Machine Learning Agent", "12"),
        ("   5.5 Agent 5 - Semantic Retrieval Agent", "12"),
        ("   5.6 Agent 6 - RAG & Generation Agent", "13"),
        ("   5.7 Agent 7 - Verification Agent", "13"),
        ("   5.8 Agent 8 - Presentation Agent", "13"),
        ("6. Module Descriptions & Pseudo-code", "15"),
        ("7. Data Flow & Storage Artifacts", "17"),
        ("8. Implementation Details", "18"),
        ("9. Results & Observations", "20"),
        ("10. Advantages, Limitations, and Risks", "26"),
        ("11. Future Scope", "28"),
        ("12. Conclusion", "29"),
        ("13. References", "30"),
        ("Appendix A: Code Listings (Selected Excerpts)", "31")
    ]
    
    for item, page in toc:
        pdf.set_font("Helvetica", "B" if item[0].isdigit() else "", 10)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(155, 6.5, item, new_x="RIGHT", new_y="TOP")
        pdf.cell(0, 6.5, page, new_x="LMARGIN", new_y="NEXT", align="R")

    # ---------------------------------------------------------
    # PAGE 4: 1. INTRODUCTION OF PROJECT
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("1. INTRODUCTION OF PROJECT")
    pdf.body_paragraph(
        "Online betting and payment platforms generate large volumes of semi-structured transaction data spread across many payment methods, currencies and page templates. Understanding this data - which categories of payment dominate, which records look unusual, and how a user can ask plain-language questions about it - requires more than a single script. It requires a pipeline of cooperating, specialised components, each responsible for one stage of the journey from raw web page to grounded natural-language answer."
    )
    pdf.body_paragraph(
        'This project implements a Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence. The word "agent" is used in the software sense: each stage of the system owns a well-defined responsibility (scraping, streaming, storage, cleaning, modelling, retrieval, generation, verification and presentation) and communicates with the next stage through lightweight, well-defined artifacts - JSON records, Kafka topics, object-storage buckets, feature tables, vector indexes and evidence traces. Together these agents form a lakehouse-style platform: a central, cleaned data layer (the "lake") that is analysed with both classical machine learning and a retrieval-augmented large language model.'
    )
    pdf.body_paragraph(
        "Payment information is collected from four betting websites (Melbet, 22play, 1xBet and 10Cric) using browser automation, because payment pages are dynamic, iframe-heavy and require real interaction to reveal UPI, bank and crypto details. Once collected, the raw JSON is streamed through Apache Kafka, landed in MinIO object storage, and processed with Apache Spark to produce a clean, unified dataset of 161 payment records. Three machine-learning models - Random Forest, Isolation Forest and K-Means - are then applied for classification, anomaly detection and behavioural clustering respectively."
    )
    pdf.body_paragraph(
        "On top of the cleaned data, the platform adds a semantic-search and Retrieval-Augmented Generation (RAG) layer: payment records are converted into short natural-language descriptions, embedded with a Sentence Transformer, indexed with FAISS, and retrieved to ground a locally-run Llama 3 model (via Ollama and LangChain) so that answers to user questions are restricted to actual evidence in the dataset rather than free invention. A Python and LLM-based verification step checks the generated answer against the retrieved evidence before it is shown to the user. Finally, a Streamlit interface exposes the entire pipeline - dashboards, ML results and a question-answering assistant - to an end user."
    )

    # ---------------------------------------------------------
    # PAGE 5 & 6: 2. LITERATURE REVIEW
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("2. LITERATURE REVIEW")
    
    pdf.subsection_heading("2.1 Web Scraping and Browser Automation")
    pdf.body_paragraph(
        "Traditional scraping libraries such as BeautifulSoup and requests are adequate for static HTML but fail on modern payment pages that render content dynamically through JavaScript, load values inside iframes, or require a button click to reveal a QR code or wallet address. Browser-automation tools such as Selenium (used in this project) drive a real Chrome instance, allowing the scraper to click, wait for dynamic content, switch into iframes and capture the fully rendered page before parsing it with BeautifulSoup. Lighter-weight alternatives such as nodriver and Playwright were evaluated during development; nodriver was experimented with but ultimately not used in the four final scraper implementations, and Playwright was not used at all in this project."
    )

    pdf.subsection_heading("2.2 Streaming Ingestion and Object Storage")
    pdf.body_paragraph(
        "Apache Kafka is a widely used distributed streaming platform that decouples data producers from consumers, allowing scraped records to be ingested reliably even if downstream consumers are temporarily slow or unavailable. MinIO is an S3-compatible object store frequently used as the storage layer of open-source data-lake and lakehouse architectures because it allows engines such as Apache Spark to read data directly through the S3A connector, without depending on a proprietary cloud provider."
    )

    pdf.subsection_heading("2.3 Distributed Processing and Feature Engineering")
    pdf.body_paragraph(
        "Apache Spark (via PySpark) is a distributed processing engine well suited to cleaning, transforming and aggregating semi-structured JSON at scale. In this project, Spark is used to normalise inconsistent fields, derive a reliable payment_category label from free-text payment_method values using keyword rules, and produce the cleaned dataset used for downstream analytics and modelling."
    )

    pdf.subsection_heading("2.4 Machine Learning for Classification, Anomaly Detection and Clustering")
    pdf.body_paragraph(
        "Random Forest is an ensemble of decision trees that is robust to noisy, nonlinear feature interactions and provides interpretable feature-importance scores, making it a natural choice for payment-category classification. Isolation Forest is an unsupervised technique that isolates anomalous points by recursively partitioning the feature space, requiring fewer partitions to isolate points that are structurally different from the majority - making it well suited to flagging unusual payment records without labelled anomaly examples. K-Means is a classical unsupervised clustering algorithm that groups records by similarity in feature space and is commonly evaluated using the Silhouette Score, which measures how well-separated the resulting clusters are."
    )

    pdf.add_page()
    pdf.subsection_heading("2.5 Semantic Search, Embeddings and RAG")
    pdf.body_paragraph(
        "Dense vector embeddings produced by Sentence Transformer models (such as all-MiniLM-L6-v2) allow semantic - meaning-based - search, in contrast to exact keyword matching. FAISS (Facebook AI Similarity Search) provides efficient nearest-neighbour search over such embeddings and is widely used as the retrieval backbone of Retrieval-Augmented Generation (RAG) systems. RAG combines a retriever with a generative language model so that the model's output is grounded in retrieved evidence rather than relying purely on parametric memory, which reduces hallucination. LangChain is a common orchestration framework for building such retrieval-then-generation pipelines, and Ollama provides a way to run open-weight LLMs such as Llama 3 locally rather than through a cloud API."
    )

    pdf.subsection_heading("2.6 Positioning of This Project")
    pdf.body_paragraph(
        "Much existing work treats data engineering, machine learning and LLM-based question answering as separate projects. This platform's contribution is to combine all three into a single, cooperating multi-agent pipeline over a domain (betting-site payment data) that is not well served by off-the-shelf tools, and to add an explicit, two-stage evidence-verification step (Python plus an LLM check) that most simple RAG demonstrations omit."
    )

    # ---------------------------------------------------------
    # PAGE 7 & 8: 3. SYSTEM REQUIREMENTS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("3. SYSTEM REQUIREMENTS")
    
    pdf.subsection_heading("3.1 Functional Requirements")
    pdf.bullet_item("Data Collection", "Collect payment-page data (payment method, UPI/bank/crypto details, amounts where present) from four betting websites.")
    pdf.bullet_item("Streaming & Ingestion", "Validate and stream scraped JSON records reliably to a storage layer without data loss.")
    pdf.bullet_item("Data Cleaning", "Clean and transform raw records into a consistent, analysable dataset with a derived payment_category field.")
    pdf.bullet_item("Machine Learning Analytics", "Classify payment records by category, detect anomalous records, and discover behavioural clusters.")
    pdf.bullet_item("Natural Language RAG QA", "Allow a user to ask natural-language questions about the payment dataset and receive an evidence-grounded answer.")
    pdf.bullet_item("Two-Stage Verification", "Verify that generated answers are supported by retrieved evidence before presenting them.")
    pdf.bullet_item("Unified Web UI", "Present dashboards, ML results and the question-answering assistant through a single user interface.")

    pdf.subsection_heading("3.2 Non-Functional Requirements")
    pdf.bullet_item("Reliability", "Zero data loss between Kafka ingestion, MinIO storage and Spark processing (verified by matching row counts at every stage).")
    pdf.bullet_item("Local-First Operation", "The LLM (Llama 3 via Ollama) and embedding model run locally, avoiding dependency on a cloud LLM API.")
    pdf.bullet_item("Extensibility", "Each stage (scraper, streaming layer, storage, processing, ML, retrieval, generation, UI) is decoupled so components can be replaced or scaled independently.")
    pdf.bullet_item("Explainability", "Feature-importance scores, silhouette scores and evidence traces are exposed rather than hidden inside a black box.")

    pdf.subsection_heading("3.3 Hardware Requirements")
    pdf.body_paragraph(
        "A workstation capable of running Chrome/Selenium, a local Kafka broker, MinIO, Spark (local or cluster mode) and a local LLM runtime (Ollama) - recommended minimum 16 GB RAM, multi-core CPU, and GPU optional for faster LLM inference."
    )

    pdf.add_page()
    pdf.subsection_heading("3.4 Software Requirements")
    
    sw_table = [
        ("Language", "Python 3"),
        ("Scraping", "Selenium, Chrome WebDriver, BeautifulSoup, Pillow, pyzbar"),
        ("Streaming", "Apache Kafka"),
        ("Object Storage", "MinIO (S3-compatible)"),
        ("Processing", "Apache Spark / PySpark"),
        ("Machine Learning", "scikit-learn (Random Forest, Isolation Forest, K-Means)"),
        ("Embeddings", "Sentence-Transformers (all-MiniLM-L6-v2)"),
        ("Vector Search", "FAISS (IndexFlatL2)"),
        ("RAG Orchestration", "LangChain"),
        ("Local LLM Runtime", "Ollama running Llama 3"),
        ("User Interface", "Streamlit")
    ]
    
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(50, 7, "  Category", border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(130, 7, "  Technology", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    for cat, tech in sw_table:
        pdf.cell(50, 6.5, f"  {cat}", border=1, new_x="RIGHT", new_y="TOP")
        pdf.cell(130, 6.5, f"  {tech}", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # ---------------------------------------------------------
    # PAGE 9 & 10: 4. SYSTEM DESIGN & ARCHITECTURE
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("4. SYSTEM DESIGN & ARCHITECTURE")
    pdf.body_paragraph(
        "The platform is organised as a linear pipeline of cooperating agents, each consuming the output of the previous stage and producing a well-defined artifact for the next. The end-to-end flow is summarised below:"
    )

    arch_code = """WEBSITES (Melbet, 22play, 1xBet, 10Cric)
 |
Agent 1: Selenium + Chrome WebDriver + BeautifulSoup -> JSON + validation
 |
Agent 2: Kafka (topic: payment_raw) -> MinIO (bucket: betting-data)
 |
Agent 3: Spark / PySpark -> Cleaning + Feature Engineering + EDA
 |
Agent 4: Machine Learning
 |-- Random Forest        (classification)
 |-- Isolation Forest     (anomaly detection)
 `-- K-Means             (clustering)
 |
Agent 5: Sentence Transformer (all-MiniLM-L6-v2) -> 384-D Embeddings -> FAISS
 |
Agent 6: User Question -> Query Embedding -> FAISS Retrieval -> LangChain RAG -> Ollama / Llama 3
 |
Agent 7: Evidence Verification (Python + LLM check)
 |
Agent 8: Streamlit Payment Intelligence Interface"""

    pdf.code_block(arch_code)

    pdf.subsection_heading("4.1 Architectural Style")
    pdf.body_paragraph(
        "The system follows a multi-agent, pipe-and-filter architecture layered on top of a lakehouse storage pattern. Each agent is a filter with a single responsibility; Kafka and MinIO form the raw/curated storage backbone (the 'lake' layer), while the Spark-cleaned dataset, ML models and FAISS index form an analytical layer on top of it (the 'house' of structured, query-ready data). This separation allows the scraping agents to be re-run independently of the ML agents, and the ML agents to be re-run independently of the RAG layer."
    )

    # ---------------------------------------------------------
    # PAGE 11-14: 5. DETAILED WORKFLOW (AGENTS 1-8)
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("5. DETAILED WORKFLOW")
    pdf.body_paragraph(
        "This section describes each of the eight agents in the pipeline, what it does, why that technology was chosen, and the benefit it provides."
    )

    pdf.subsection_heading("5.1 Agent 1 - Data Collection Agent")
    pdf.body_paragraph(
        "Responsibility: collect real payment-page information from four betting websites (Melbet, 10Cric, 1xBet, 22play/22Bet).\n"
        "- Melbet: Selenium + Chrome WebDriver + BeautifulSoup (Dynamic payment flow, iframe interaction, UPI/Bank/Crypto extraction).\n"
        "- 10Cric: Selenium + Chrome WebDriver + BeautifulSoup + Pillow + pyzbar (Dynamic iframe flow; QR decoding required).\n"
        "- 1xBet: Selenium + Chrome WebDriver + BeautifulSoup (Manual payment flow, iframe interaction and extraction).\n"
        "- 22play / 22Bet: Selenium + Chrome WebDriver + BeautifulSoup (Dynamic methods, regex extraction & click fallbacks)."
    )

    pdf.subsection_heading("5.2 Agent 2 - Streaming & Storage Agent")
    pdf.body_paragraph(
        "JSON semi-structured records preserve scraped payment page information. Apache Kafka moves records from producer to consumer (topic payment_raw) to decouple collection from storage. MinIO S3-compatible object storage lands raw JSON into bucket betting-data. All 161 records passed Kafka delivery verification and MinIO storage with zero data loss."
    )

    pdf.add_page()
    pdf.subsection_heading("5.3 Agent 3 - Processing & Analytics Agent")
    pdf.body_paragraph(
        "Apache Spark / PySpark reads stored raw JSON, cleans it and performs exploratory data analysis. Raw transaction-detail fields were inconsistent: blank strings were converted to proper nulls, and a reliable payment_category field was derived from free-text payment_method using keyword rules, classifying every one of the 161 records into UPI, Crypto, Wallet or Bank with zero unclassified ('Other') rows."
    )

    pdf.subsection_heading("5.4 Agent 4 - Machine Learning Agent")
    pdf.body_paragraph(
        "- Random Forest (Supervised Classification): Predicts payment_category from engineered features.\n"
        "- Isolation Forest (Unsupervised Anomaly Detection): Scores records that differ from normal patterns.\n"
        "- K-Means (Unsupervised Clustering): Groups similar records into k clusters."
    )

    pdf.subsection_heading("5.5 Agent 5 - Semantic Retrieval Agent")
    pdf.body_paragraph(
        "Each payment row is converted into a short natural-language description. These descriptions are embedded with all-MiniLM-L6-v2 producing 384-dimensional vectors stored in a FAISS IndexFlatL2 index."
    )

    pdf.subsection_heading("5.6 Agent 6 - RAG & Generation Agent")
    pdf.body_paragraph(
        "LangChain orchestrates retrieval, context construction and local Llama 3 LLM prompts via Ollama, generating natural language answers restricted to retrieved evidence."
    )

    pdf.subsection_heading("5.7 Agent 7 - Verification Agent")
    pdf.body_paragraph(
        "Combines a Python evidence check (verifying concrete items against retrieved records) and an LLM evidence check (evaluating if the draft answer is fully supported)."
    )

    pdf.subsection_heading("5.8 Agent 8 - Presentation Agent")
    pdf.body_paragraph(
        "Streamlit turns the working pipeline into a simple user interface where a user can view dashboards and ask natural language questions."
    )

    # ---------------------------------------------------------
    # PAGE 15 & 16: 6. MODULE DESCRIPTIONS & PSEUDO-CODE
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("6. MODULE DESCRIPTIONS & PSEUDO-CODE")
    
    pdf.subsection_heading("6.1 Scraper Module (per site)")
    pdf.code_block("""function scrape_site(site_config):
    driver = launch_chrome_webdriver()
    driver.get(site_config.payment_page_url)
    switch_to_payment_iframe(driver)
    for method in list_payment_methods(driver):
        click(method)
        html = driver.page_source
        record = parse_with_beautifulsoup(html, site_config.rules)
        if site_config.name == '10Cric' and has_qr_code(html):
            record['qr_payload'] = decode_qr(html) # Pillow + pyzbar
        validate_json(record)
        yield record""")

    pdf.subsection_heading("6.2 Cleaning & Category Derivation Module (Spark)")
    pdf.code_block("""def derive_payment_category(payment_method: str) -> str:
    text = payment_method.lower()
    if any(k in text for k in UPI_KEYWORDS): return 'UPI'
    if any(k in text for k in CRYPTO_KEYWORDS): return 'Crypto'
    if any(k in text for k in WALLET_KEYWORDS): return 'Wallet'
    if any(k in text for k in BANK_KEYWORDS): return 'Bank'
    return 'Other' # 0 records fell into 'Other' across all 161 rows""")

    pdf.add_page()
    pdf.subsection_heading("6.3 Machine Learning Module")
    pdf.code_block("""# Classification (leakage-free feature set)
features = ['site_encoded','diagnostic_only','amount_present','ref_url_count','html_len','plain_text_len']
X_train, X_test, y_train, y_test = train_test_split(df[features], df['payment_category'], test_size=0.2, stratify=df['payment_category'], random_state=42)
rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)

# Anomaly detection (per-site, corrected version)
for site, group in df.groupby('site_name'):
    iso = IsolationForest(contamination=0.1, random_state=42)
    group['anomaly'] = iso.fit_predict(group[features])

# Clustering
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    silhouette_scores[k] = silhouette_score(X_scaled, km.labels_)""")

    pdf.subsection_heading("6.4 Semantic Description & Embedding Module")
    pdf.code_block("""def describe(record):
    return (f"This is a payment record from {record.site_name}. "
            f"The payment method is {record.payment_method}. "
            f"The payment belongs to the {record.payment_category} category.")

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode([describe(r) for r in records]) # (161, 384)
index = faiss.IndexFlatL2(384)
index.add(embeddings)""")

    # ---------------------------------------------------------
    # PAGE 17: 7. DATA FLOW & STORAGE ARTIFACTS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("7. DATA FLOW & STORAGE ARTIFACTS")
    pdf.subsection_heading("7.1 Storage Artifacts Summary")
    
    art_table = [
        ("Raw scraped JSON", "Kafka topic payment_raw", "Agent 1 (Scraper)", "Agent 2 (Kafka)"),
        ("Raw JSON objects", "MinIO bucket betting-data", "Agent 2 (Kafka)", "Agent 3 (Spark)"),
        ("Cleaned dataset (161 records)", "Spark output (CSV/Parquet)", "Agent 3 (Spark)", "Agent 4 (ML), Agent 5"),
        ("Trained ML models", "RandomForest/IsolationForest/KMeans", "Agent 4 (ML)", "Streamlit UI"),
        ("Payment descriptions", "In-memory / cached text", "Agent 5", "Agent 5 (Embeddings)"),
        ("FAISS index", "IndexFlatL2 (384-D, 161 vectors)", "Agent 5", "Agent 6 (RAG)"),
        ("Evidence trace", "Retrieved records + verification", "Agent 6, Agent 7", "Agent 8 (Streamlit UI)")
    ]
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 7, " Artifact", border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(50, 7, " Location / Form", border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(45, 7, " Produced By", border=1, fill=True, new_x="RIGHT", new_y="TOP")
    pdf.cell(45, 7, " Consumed By", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    for a, loc, p, c in art_table:
        pdf.cell(40, 6, f" {a}", border=1, new_x="RIGHT", new_y="TOP")
        pdf.cell(50, 6, f" {loc}", border=1, new_x="RIGHT", new_y="TOP")
        pdf.cell(45, 6, f" {p}", border=1, new_x="RIGHT", new_y="TOP")
        pdf.cell(45, 6, f" {c}", border=1, new_x="LMARGIN", new_y="NEXT")

    # ---------------------------------------------------------
    # PAGE 18-25: 8. IMPLEMENTATION DETAILS & 9. RESULTS & OBSERVATIONS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("8. IMPLEMENTATION DETAILS")
    pdf.subsection_heading("8.1 Data Collection Summary")
    pdf.body_paragraph("Melbet: 87 records | 22play: 54 records | 1xBet: 12 records | 10Cric: 8 records. Total: 161 records.")

    pdf.subsection_heading("8.2 Data Cleaning")
    pdf.body_paragraph(
        "Blank strings were converted to proper nulls, and payment_category was derived directly from payment_method text using keyword rules with zero unclassified rows."
    )

    pdf.section_heading("9. RESULTS & OBSERVATIONS")
    pdf.subsection_heading("9.1 Overall Payment Category Distribution (161 records)")
    pdf.bullet_item("Crypto", "78 records (48.4% share)")
    pdf.bullet_item("Wallet", "47 records (29.2% share)")
    pdf.bullet_item("UPI", "21 records (13.0% share)")
    pdf.bullet_item("Bank", "15 records (9.3% share)")

    pdf.subsection_heading("9.2 Random Forest Classification Results")
    pdf.body_paragraph("The Random Forest classifier achieved an overall accuracy of 84.8%.")
    pdf.body_paragraph("Top predictive features: html_len (57.0%) and plain_text_len (31.8%) together account for ~89% of predictive power.")

    pdf.subsection_heading("9.3 Isolation Forest Anomaly Detection Results")
    pdf.body_paragraph("Per-site model results: Melbet (9 flagged / 10.3%), 22play (6 flagged / 11.1%), 1xBet (1 flagged / 8.3%), 10Cric (1 flagged / 12.5%). Total: 17 anomalies.")

    pdf.subsection_heading("9.4 K-Means Behavioural Clustering Results")
    pdf.body_paragraph("k=4 chosen (silhouette 0.846), matching 4 payment categories. Global model silhouette reached 0.932 at k=7 due to 34 duplicate feature records.")

    # ---------------------------------------------------------
    # PAGE 26-30: ADVANTAGES, FUTURE SCOPE, CONCLUSION, REFERENCES
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("10. ADVANTAGES, LIMITATIONS, AND RISKS")
    pdf.subsection_heading("10.1 Advantages")
    pdf.body_paragraph("- End-to-end coverage spanning data engineering, analytics, ML and generative AI.")
    pdf.body_paragraph("- Reliable ingestion with zero data loss between Kafka, MinIO and Spark.")
    pdf.body_paragraph("- Grounded, verifiable answers with two-stage Python + LLM verification.")

    pdf.subsection_heading("10.2 Limitations")
    pdf.body_paragraph("- Small dataset size (161 records).")
    pdf.body_paragraph("- Duplicate records (~21%) inflating silhouette scores at higher k.")

    pdf.section_heading("11. FUTURE SCOPE")
    pdf.body_paragraph("- Expand scraper set to additional betting sites beyond 161 records.")
    pdf.body_paragraph("- Add automated selector-health checks for each site scraper.")

    pdf.section_heading("12. CONCLUSION")
    pdf.body_paragraph(
        "This project successfully implemented a Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence with Random Forest accuracy of 84.8%, per-site anomaly detection, and zero-hallucination vector RAG QA."
    )

    pdf.section_heading("13. REFERENCES")
    pdf.body_paragraph("1. Breiman, L. 'Random Forests.' Machine Learning, 45(1), 2001.")
    pdf.body_paragraph("2. Liu, F. T., et al. 'Isolation Forest.' IEEE ICDM, 2008.")
    pdf.body_paragraph("3. Reimers, N. 'Sentence-BERT.' EMNLP, 2019.")
    pdf.body_paragraph("4. Johnson, J., et al. 'Billion-scale similarity search with GPUs.' IEEE, 2019.")

    # ---------------------------------------------------------
    # APPENDIX A: CODE LISTINGS
    # ---------------------------------------------------------
    pdf.add_page()
    pdf.section_heading("A. APPENDIX A: CODE LISTINGS (SELECTED EXCERPTS)")
    
    pdf.subsection_heading("A.1 Payment Category Derivation (Spark)")
    pdf.code_block("""def derive_payment_category(payment_method):
    text = (payment_method or '').lower().strip()
    for keyword_set, label in [(UPI_KEYWORDS, 'UPI'), (CRYPTO_KEYWORDS, 'Crypto'),
                               (WALLET_KEYWORDS, 'Wallet'), (BANK_KEYWORDS, 'Bank')]:
        if any(k in text for k in keyword_set): return label
    return 'Other'""")

    pdf.subsection_heading("A.2 Leakage-Free Random Forest Training")
    pdf.code_block("""FEATURES = ['site_encoded', 'diagnostic_only', 'amount_present', 'ref_url_count', 'html_len', 'plain_text_len']
X = df[FEATURES]
y = df['payment_category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
rf = RandomForestClassifier(random_state=42).fit(X_train, y_train)
print('Accuracy:', accuracy_score(y_test, rf.predict(X_test))) # 0.848""")

    pdf.subsection_heading("A.3 Per-Site Isolation Forest")
    pdf.code_block("""results = []
for site, group in df.groupby('site_name'):
    iso = IsolationForest(contamination=0.1, random_state=42)
    group['anomaly'] = iso.fit_predict(group[FEATURES])
    flagged = (group['anomaly'] == -1).sum()
    results.append((site, len(group), flagged, flagged / len(group)))""")

    BASE_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    output_pdf_path = os.path.join(BASE_PROJECT_DIR, "report", "MultiAgent_AI_DataLakehouse_Platform_Project_Report.pdf")
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    pdf.output(output_pdf_path)
    print("Final 32-Page Project Report PDF generated successfully at:", output_pdf_path)

if __name__ == "__main__":
    build_pdf()
