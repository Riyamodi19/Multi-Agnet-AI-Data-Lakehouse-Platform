# Phase 1: Data Acquisition & Web Scraping

## Overview
This folder contains the automated web scraping architecture developed using **Python, Playwright, Scrapy, and BeautifulSoup** to extract dynamic payment options and details from multiple online betting sites.

## Target Platforms Scraped
1. **Melbet**: Scraped 180 pages / 170 JSON payment dumps.
2. **22Bet**: Scraped 211 JSON payment dumps.
3. **10Cric**: Scraped 126 JSON payment dumps.
4. **1xBet**: Scraped 52 JSON payment dumps.

## Extracted Data Fields
- `site_name`: Platform name (10Cric, Melbet, 22Bet, 1xBet)
- `payment_method`: Target payment method extracted
- `html`: Complete raw HTML document body (containing dynamic payment cell DOM elements)
- `plain_text`: Extracted inner text content
- `transaction_details`: Extracted dictionary containing `upi_id`, `upi_name`, `bank_account_number`, `ifsc_code`
- `fetchtime`: UTC timestamp of extraction
- `screenshots`: Target page rendering verification screenshots

## Directory Layout
- `scrappingcode/`: Python scrapers (`melbet.py`, `payment_scraper.py`, `1bet_robust_scraper.py`, `automated_scraping.py`)
- `10crick/`: Spiders and outputs for 10Cric
- `1xbet/`: Spiders and outputs for 1xBet
- `22xbet/`: Spiders and outputs for 22Bet
- `melbet/`: Spiders and outputs for Melbet
- `outputs/`: Unified output directory for scraped JSON payloads
