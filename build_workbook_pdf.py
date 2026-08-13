"""
Generate a Simple, Structured PDF Workbook for the Presentation Defense Walkthrough
Title: Multi-Agent AI Data Lakehouse Presentation Defense Workbook
Target Output: d:\\final_end_game\\report\\MultiAgent_AI_DataLakehouse_Presentation_Workbook.pdf
"""

import os
from fpdf import FPDF

class PresentationWorkbookPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "Multi-Agent AI Data Lakehouse - Presentation Defense Workbook", border=False, new_x="LMARGIN", new_y="NEXT", align="R")
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

    def slide_header(self, slide_num, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(147, 51, 234) # Purple
        self.cell(0, 10, f"SLIDE {slide_num}: {title.upper()}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(147, 51, 234)
        self.set_line_width(0.6)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

    def section_label(self, label):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(30, 41, 59) # Slate 800
        self.cell(40, 6, f"{label}:", new_x="RIGHT", new_y="TOP")

    def section_body(self, text):
        clean_text = text.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-").replace("➔", "->").replace("🗣️", "*").replace("🚨", "ALERT:").replace("💡", "SOLUTION:").replace("⚙️", "*").replace("📊", "*").replace("🔍", "*").replace("🔒", "*").replace("⚡", "*")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 65, 85) # Slate 700
        self.multi_cell(0, 5.5, clean_text)
        self.ln(2)

    def spoken_script_box(self, text):
        clean_text = text.replace("—", "-").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'").replace("•", "-").replace("➔", "->").replace("🗣️", "*")
        self.set_font("Helvetica", "I", 9.5)
        self.set_text_color(15, 23, 42) # Slate 900
        self.set_fill_color(245, 247, 250) # Very light gray
        self.set_draw_color(147, 51, 234) # Purple left border
        self.set_line_width(0.5)
        
        # Calculate lines and render a nice box with a left vertical border
        lines = self.multi_cell(0, 5, f'"{clean_text.strip()}"', border=0, fill=True, dry_run=True, output="LINES")
        box_height = len(lines) * 5 + 4
        
        x = self.get_x()
        y = self.get_y()
        
        # Draw background and left border line
        self.rect(x, y, 180, box_height, style="F")
        self.line(x, y, x, y + box_height)
        
        self.set_xy(x + 4, y + 2)
        self.multi_cell(172, 5, f'"{clean_text.strip()}"', border=0)
        self.set_xy(x, y + box_height + 4)

def build_pdf():
    pdf = PresentationWorkbookPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover Page
    pdf.add_page()
    pdf.set_draw_color(30, 41, 59)
    pdf.set_line_width(1)
    pdf.rect(10, 10, 190, 277)
    
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "C-DAC Hyderabad - DBDA Project 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(147, 51, 234)
    pdf.multi_cell(0, 8, "Multi-Agent AI Data Lakehouse Platform for\nBetting Site Data Intelligence", align="C")
    pdf.ln(20)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, "PRESENTATION ORAL SCRIPT & TECHNICAL DEFENSE WORKBOOK", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 8, "(Slides 1-9 & 16-24 Walkthrough)", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(25)
    
    # Team Details block
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.cell(0, 6, "Guided By: Ms. Krishnaveni", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    pdf.cell(0, 6, "Presented By Team BDA:", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 10.5)
    pdf.cell(0, 6.5, "Ms. Riya Modi (260250325032)", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6.5, "Mr. Sri Charan (260250325017)", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6.5, "Mr. Prasad P. Gautre (260250325029)", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6.5, "Mr. Niraj S. Kadam (260250325025)", new_x="LMARGIN", new_y="NEXT", align="C")

    # SLIDE 1
    pdf.add_page()
    pdf.slide_header("1", "Cover Page / Title Slide")
    pdf.section_label("What It Is")
    pdf.section_body("The introductory slide of the presentation containing project title, guide name, BDA course details, and team presenter names.")
    pdf.section_label("Why This Project?")
    pdf.section_body("Digital payment tracking is critical for financial intelligence. Betting platforms constantly rotate bank accounts and UPI IDs to bypass regulatory bans. This project builds an automated platform to track and analyze these rotated accounts in real-time.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Good morning/afternoon, respected guide Ms. Krishnaveni and members of the evaluation panel. I am Riya Modi, and along with my team members-Sri Charan, Prasad Gautre, and Niraj Kadam-we are presenting our final BDA project: 'Multi-Agent AI Data Lakehouse Platform for Betting Site Data Intelligence'.\n\nWe chose this project to automate the detection and tracking of rotated merchant payment methods across dynamic betting websites in real-time."
    )

    # SLIDE 2
    pdf.add_page()
    pdf.slide_header("2", "Problem Statement")
    pdf.section_label("What It Is")
    pdf.section_body("The core challenges the project addresses, covering dynamic layouts, endpoint rotation, and DOM noise.")
    pdf.section_label("How It Works")
    pdf.section_body("Online platforms hide payment options in dynamic scripts/iframes and rotate them frequently to avoid bans. Manual verification is slow and does not scale.")
    pdf.section_label("Why This")
    pdf.section_body("Standard database queries or single-site scrapers fail. We built a coordinated, multi-agent pipeline to decouple web collection from storage and risk modeling.")
    pdf.section_label("Why Not Other")
    pdf.section_body("Static SQL databases cannot handle dynamic website layout changes without schema crashes. Medallion architecture partitions raw data from refined tables.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Betting platforms hide payment gateways inside dynamic web layouts and nested iframes, and frequently rotate their UPI IDs and wallets to avoid bans. This results in noisy, duplicate records.\n\nChecking these sites manually is slow, error-prone, and cannot scale. As shown in the workflow diagram below, our platform automates the entire process: scraping dynamic pages, streaming with Kafka, storage in a Lakehouse, and risk intelligence using ML and RAG."
    )

    # SLIDE 3
    pdf.add_page()
    pdf.slide_header("3", "Project Objectives")
    pdf.section_label("What It Is")
    pdf.section_body("The defined goals and roadmap of the Multi-Agent AI Data Lakehouse Platform.")
    pdf.section_label("How It Works")
    pdf.section_body("A step-by-step pipeline from raw web ingestion to clean storage, risk modeling, and a local RAG assistant.")
    pdf.section_label("Why This")
    pdf.section_body("Follows the industry-standard Medallion pipeline (Ingest -> Stream -> Clean -> Model -> Search -> Verify -> Visualize) ensuring data quality at each layer.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Our primary goals are: first, automate dynamic data extraction; second, stream records via Kafka with zero data loss; third, organize data into raw Bronze and clean Silver Parquet formats via MinIO; fourth, apply Machine Learning to predict categories and detect anomalies; and finally, host a local Llama 3 RAG QA panel inside a Streamlit dashboard."
    )

    # SLIDE 4
    pdf.add_page()
    pdf.slide_header("4", "System Overview Workflow")
    pdf.section_label("What It Is")
    pdf.section_body("The end-to-end processing pipeline architecture showing data transformations.")
    pdf.section_label("How It Works")
    pdf.section_body("Web Scraper -> Kafka Topic -> MinIO Bronze -> PySpark Silver -> Scikit-Learn ML -> FAISS Index -> LangChain local RAG -> Two-stage Verification -> Streamlit UI.")
    pdf.section_label("Why This")
    pdf.section_body("Decoupling components. If a web scraper encounters a layout change, the Kafka queue caches the message streams, keeping the downstream database, ML, and dashboard running.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "This slide represents our system overview workflow. Raw scraped data is sent as JSON messages through Kafka to land in our MinIO Bronze S3 store. PySpark cleans this data and writes it to Silver Parquet. Scikit-learn trains our risk models, while the records are embedded into a FAISS vector database. LangChain then retrieves this context to feed our local LLM."
    )

    # SLIDE 5
    pdf.add_page()
    pdf.slide_header("5", "Technology Stack Matrix")
    pdf.section_label("What It Is")
    pdf.section_body("A matrix of the open-source libraries and enterprise components used in the pipeline.")
    pdf.section_label("Why This")
    pdf.section_body("MinIO provides local S3-compatible storage. PySpark provides in-memory computing for cleaning. Ollama/Llama 3 runs on-premises to ensure complete privacy.")
    pdf.section_label("Why Not Other")
    pdf.section_body("AWS/Databricks charge heavy fees; MinIO/Spark are free. OpenAI APIs require sending bank details to external servers, violating GDPR/PCI-DSS rules. Local LLMs are completely secure.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Here is our technology matrix. We chose a 100% open-source stack that runs locally on standard hardware. By using local Llama 3 via Ollama, we keep all merchant bank accounts and UPI IDs private on-premises with zero cloud API costs."
    )

    # SLIDE 6
    pdf.add_page()
    pdf.slide_header("6", "The 6-Agent Platform Architecture")
    pdf.section_label("What It Is")
    pdf.section_body("The multi-agent design dividing responsibilities across 6 specialized software agents.")
    pdf.section_label("How It Works")
    pdf.section_body("Coordination: Agent 1 Scrapes -> Agent 2 Streams -> Agent 3 Spark Cleans -> Agent 4 ML Runs -> Agent 5 RAG Agent (FAISS + LLM) -> Agent 6 UI Dashboard. Note: Verification Agent runs silently in the backend.")
    pdf.section_label("Why This")
    pdf.section_body("Modularity. If a website selector breaks, we only edit Agent 1's rules without touching the ML classification in Agent 4 or the RAG in Agent 5.")
    pdf.section_label("Why Not Other")
    pdf.section_body("Traditional monolithic architectures merge all code into one giant script, making debugging difficult and increasing system failure risk.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Our platform divides responsibilities across six specialized agents: Agent 1 scrapes data, Agent 2 streams it, Agent 3 cleans it, Agent 4 runs machine learning, Agent 5 handles semantic vector RAG with Llama 3, and Agent 6 serves as our master UI orchestrator. Our verification check runs implicitly in the background to ensure data security."
    )

    # SLIDE 7
    pdf.add_page()
    pdf.slide_header("7", "Complete Workflow In Brief")
    pdf.section_label("What It Is")
    pdf.section_body("A concise summary of the linear database state transitions.")
    pdf.section_label("How It Works")
    pdf.section_body("Live Site -> JSON Event -> Kafka Ingestion -> MinIO Bronze JSON -> PySpark Silver Parquet -> Machine Learning Analytics -> FAISS Indexing -> LangChain Retrieval -> Verified UI.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "This slide summarizes our workflow in brief. The data moves linearly: live site details are scraped as JSON events, streamed via Kafka into MinIO Bronze, cleaned by PySpark into Silver Parquet, analyzed by ML models, embedded into FAISS, retrieved by LangChain, and verified for the analyst UI."
    )

    # SLIDE 8
    pdf.add_page()
    pdf.slide_header("8", "Agent 1: Data Collection Scraper")
    pdf.section_label("What It Is")
    pdf.section_body("The automated data collection agent powered by Playwright and Selenium.")
    pdf.section_label("How It Works")
    pdf.section_body("Headless Chrome controls navigate betting modals, switch iframes, and pyzbar extracts UPI VPAs from canvas QR code screenshots.")
    pdf.section_label("Why This")
    pdf.section_body("Standard tools (like BeautifulSoup) cannot render JS or switch inside dynamic cross-origin iframes where payment elements reside.")
    pdf.section_label("Why Not Other")
    pdf.section_body("Requests/BeautifulSoup only load static HTML. Paid scrapers (like Browserless) cost money. Playwright and Selenium are 100% free and easily containerized.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Let's look at Agent 1, our Data Collection Scraper. It uses Playwright and Selenium to navigate dynamic modals and switch into payment iframes. It also extracts VPAs from QR codes using Pillow and pyzbar. In total, we gathered 549 raw files, deduplicating them down to 161 unique, validated payment records."
    )

    # SLIDE 9
    pdf.add_page()
    pdf.slide_header("9", "Agent 2: Streaming & Storage Agent")
    pdf.section_label("What It Is")
    pdf.section_body("The event ingestion broker managing streaming delivery to Bronze storage.")
    pdf.section_label("How It Works")
    pdf.section_body("Scrapers act as Producers publishing JSON to topic 'payment_raw'. A Consumer worker polls the topic and writes JSON to MinIO Bronze.")
    pdf.section_label("Why This")
    pdf.section_body("High-frequency scrapers can overload database writes. Kafka buffers the incoming message streams asynchronously, ensuring zero lost records.")
    pdf.section_label("Why Not Other")
    pdf.section_body("RabbitMQ deletes messages once consumed, which prevents historical re-reading. Kafka retains data on disk, enabling stream replays to rebuild the Lakehouse.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Next is Agent 2, our Ingestion Broker. It uses Apache Kafka to separate scraping from database writes. The scraper publishes raw payloads to the payment_raw topic, and a consumer saves them to MinIO Bronze storage. This guarantees zero data loss, even if our database goes offline."
    )

    # SLIDE 16
    pdf.add_page()
    pdf.slide_header("16", "Interactive Analytics Dashboard")
    pdf.section_label("What It Is")
    pdf.section_body("The Streamlit frontend analyst console exposing risk metrics.")
    pdf.section_label("How It Works")
    pdf.section_body("Reads Silver Parquet data, renders category donut charts and horizontal bar graphs, and provides a chat assistant interface.")
    pdf.section_label("Why This")
    pdf.section_body("Streamlit is written in pure Python, integrating natively with Pandas DataFrames and ML plotting libraries.")
    pdf.section_label("Why Not Other")
    pdf.section_body("React/Angular require separate frontend servers, REST APIs, and JS development, increasing project technical debt.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Ma'am, Slide 16 shows our Streamlit Interactive Analytics Dashboard. It provides KPI scorecards, donut charts, horizontal gateway bar charts, and a risk logging table. Analysts can easily filter all metrics by selecting specific betting sites from the dropdown."
    )

    # SLIDE 17
    pdf.add_page()
    pdf.slide_header("17", "Codebase Package Layout")
    pdf.section_label("What It Is")
    pdf.section_body("The repository folder hierarchy structure.")
    pdf.section_label("How It Works")
    pdf.section_body("Divided into: data_collection/ (scrapers), streaming/ (Kafka), backend/ (Spark), ml/ (ML models), rag/ (LLM), and verification/ (auditor).")
    pdf.section_label("Why This")
    pdf.section_body("Clean modularity. Allows multiple developers to work on separate modules concurrently without git conflicts.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Our codebase is structured into decoupled packages. This makes our repository clean and modular. If we need to update a scraper rule or retrain a model, we edit only that specific folder without affecting the rest of the application."
    )

    # SLIDE 18
    pdf.add_page()
    pdf.slide_header("18", "Medallion Lakehouse Data Flow")
    pdf.section_label("What It Is")
    pdf.section_body("The data flow from raw collection in Bronze to cleaned Silver.")
    pdf.section_label("How It Works")
    pdf.section_body("Bronze JSON -> Spark Cleaning -> Silver Parquet -> ML Risk -> FAISS -> RAG QA.")
    pdf.section_label("Why This")
    pdf.section_body("Running ML models or RAG vector search directly on messy scraped DOM HTML is impossible. Medallion structures the pipeline progressively.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "This is our Medallion Lakehouse data flow. Raw JSON files in the Bronze layer are refined by PySpark into Silver Parquet format. Our machine learning risk models and FAISS vector database read from this clean Silver layer, ensuring all predictions and RAG answers are factual."
    )

    # SLIDE 19
    pdf.add_page()
    pdf.slide_header("19", "Functional Results Summary")
    pdf.section_label("What It Is")
    pdf.section_body("The final performance scores and database metrics.")
    pdf.section_label("How It Works")
    pdf.section_body("Deduplication: 99.8%. Random Forest Accuracy: 84.8%. Flagged Anomalies: 17 total. RAG Grounded Accuracy: 100% verified.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "This slide summarizes our final project results: a 99.8% data deduplication rate via PySpark, an 84.8% classification accuracy via Random Forest, 17 isolated anomalies via Isolation Forest, and sub-millisecond similarity lookups using FAISS."
    )

    # SLIDE 20
    pdf.add_page()
    pdf.slide_header("20", "Key Platform Advantages")
    pdf.section_label("What It Is")
    pdf.section_body("The core architectural benefits of our local-first implementation.")
    pdf.section_label("Why This")
    pdf.section_body("Local execution via Ollama and Llama 3 keeps sensitive banking data on-premises, with zero external cloud API costs.")
    pdf.section_label("Why Not Other")
    pdf.section_body("Cloud-based APIs (OpenAI/Claude) charge per token and send sensitive payment endpoints to third-party servers, violating compliance rules.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "Our main platform advantages are sub-second processing, full audit logs, and zero data loss. By running Llama 3 locally via Ollama, we ensure complete data privacy for sensitive payment details while incurring zero cloud API costs."
    )

    # SLIDE 21
    pdf.add_page()
    pdf.slide_header("21", "Limitations & Risk Factors")
    pdf.section_label("What It Is")
    pdf.section_body("An honest evaluation of the project's current boundaries.")
    pdf.section_label("How It Works")
    pdf.section_body("Identifies DOM selector fragility, small Bank Transfer class support (15 records), and local LLM hardware requirements (16GB RAM).")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "We identified a few project limitations: web scrapers must be updated if target sites change their page layout, our direct bank transfer category had a small count of 15 records causing recall variance, and local LLMs require at least 16GB of system RAM."
    )

    # SLIDE 22
    pdf.add_page()
    pdf.slide_header("22", "Future Scope & Enhancements")
    pdf.section_label("What It Is")
    pdf.section_body("The roadmap for scaling and securing the platform.")
    pdf.section_label("1. Image OCR")
    pdf.section_body("Use Tesseract to read text off QR code screenshots, automating canvas data ingestion.")
    pdf.section_label("2. Blockchain")
    pdf.section_body("Use Web3.py to query blockchain transaction ledgers, tracing crypto money flows.")
    pdf.section_label("3. Encryption")
    pdf.section_body("Encrypt VPA and Bank columns inside Parquet using AES-256 to secure data.")
    pdf.section_label("4. MLOps")
    pdf.section_body("Automate model retraining pipelines as new payment configurations arrive.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "For future work, we plan to implement Computer Vision OCR to read QR codes, Blockchain Analytics to trace crypto wallets, AES-256 Column-Level Encryption to secure bank details, and automated model retraining as new records arrive."
    )

    # SLIDE 23
    pdf.add_page()
    pdf.slide_header("23", "Project Conclusion")
    pdf.section_label("What It Is")
    pdf.section_body("The final wrap-up of the academic project.")
    pdf.section_label("How It Works")
    pdf.section_body("Summarizes the successful integration of scraping, streaming, Spark cleaning, ML modeling, and local vector search.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "In conclusion, our project successfully integrates web scraping, real-time streaming, PySpark cleaning, ML risk modeling, and local RAG. We achieved a 99.8% deduplication rate and 84.8% classification accuracy, proving a private, secure payment intelligence platform can be built entirely on open-source tools."
    )

    # SLIDE 24
    pdf.add_page()
    pdf.slide_header("24", "Thank You")
    pdf.section_label("What It Is")
    pdf.section_body("The final slide inviting Q&A.")
    pdf.section_label("Links Provided")
    pdf.section_body("GitHub Code Repository and Streamlit Live Application URL.")
    pdf.section_label("Spoken Script")
    pdf.spoken_script_box(
        "This concludes our presentation. Our code is available on our GitHub repository, and the dashboard is hosted live on Streamlit Cloud. We thank Ms. Krishnaveni and C-DAC Hyderabad for their guidance. We are now open for questions."
    )

    # Output file
    BASE_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    output_pdf_path = os.path.join(BASE_PROJECT_DIR, "report", "MultiAgent_AI_DataLakehouse_Presentation_Workbook.pdf")
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    pdf.output(output_pdf_path)
    print("Presentation Workbook PDF generated successfully at:", output_pdf_path)

if __name__ == "__main__":
    build_pdf()
