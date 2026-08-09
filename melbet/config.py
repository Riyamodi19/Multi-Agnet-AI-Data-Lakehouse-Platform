import os
import re
import time
import json
from datetime import datetime, timezone
import urllib.parse
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

# Load environment variables
load_dotenv()

# Import configuration fallback
try:
    from config import BASE_URL
except ImportError:
    BASE_URL = "https://melbet.mobi/en"


class SimplifiedPaymentScraper:
    def __init__(self, headless=True, wait_timeout=15):
        self.wait_timeout = wait_timeout
        self.output_dir = "OUTPUT"
        self.base_url = BASE_URL
        self.all_payment_methods = []

        self.setup_output_directory()
        self.multimedia_dir = self.setup_multimedia_directory()
        self.setup_driver(headless)
        self.scraped_data = {}

    def setup_output_directory(self):
        """Create OUTPUT directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created OUTPUT directory: {self.output_dir}")
        else:
            print(f"Using existing OUTPUT directory: {self.output_dir}")

    def setup_multimedia_directory(self):
        """Create and return specialized multimedia folder within output path"""
        media_path = os.path.join(self.output_dir, "multimedia")
        if not os.path.exists(media_path):
            os.makedirs(media_path)
            print(f"Created multimedia directory: {media_path}")
        return media_path

    def setup_driver(self, headless=True):
        """Setup Chrome driver with appropriate options and stealth configuration"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL",
                fix_hairline=True)

        self.wait = WebDriverWait(self.driver, self.wait_timeout)

    def perform_login(self):
        print("Manual login mode enabled")

        self.driver.get(self.base_url)

        print("\nSTEP 1: Login manually")
        print("STEP 2: Open Deposit/Cashier page manually")
        print("STEP 3: Make sure payment methods are visible")
        print("STEP 4: Then come back to terminal")

        input("\nPress ENTER only after payment methods are visible...")

        return True

            

    def wait_for_page_load(self):
        """Wait for page to be completely loaded"""
        try:
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(2)
        except TimeoutException:
            print("Page load timeout - continuing anyway")

    def switch_to_payment_iframe(self):
        """Find and switch to payment iframe"""
        self.driver.switch_to.default_content()
        
        iframe_selectors = [
            "iframe[name*='payment']",
            "iframe[id*='payment']",
            "iframe[src*='paysystem']",
            "iframe[src*='deposit']",
            "iframe#payments_frame",
            "iframe[name*='17564400901360660812']"
        ]

        for selector in iframe_selectors:
            try:
                iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                self.driver.switch_to.frame(iframe)
                print(f"Switched to payment iframe: {selector}")
                self.wait_for_page_load()
                return True
            except (TimeoutException, NoSuchElementException):
                continue

        print("No payment iframe found")
        return False

    def extract_payment_methods(self):
        payment_elements = []

        selectors = [
        ".payment-cell",
        ".payment_item",
        "[data-method]",
        "[data-icon]",
        ".payment-cell--recommended"
    ]

        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

                print(f"Selector {selector} -> {len(elements)} elements")

                if len(elements) > 0:
                    payment_elements = elements
                    break

            except Exception as e:
                print(f"Error with selector {selector}: {e}")

        return payment_elements

    def extract_payment_name(self, element):
        """Extract payment method name"""
        try:
            name_selectors = [
                ".payment-cell-name__caption",
                ".payment_item__name",
                ".payment-cell__name",
                "[title]"
            ]

            payment_name = "Unknown"
            for name_selector in name_selectors:
                try:
                    name_element = element.find_element(By.CSS_SELECTOR, name_selector)
                    payment_name = name_element.get_attribute('title') or name_element.text.strip()
                    if payment_name:
                        break
                except NoSuchElementException:
                    continue

            return payment_name
        except Exception:
            return "Unknown"

    def click_payment_method(self, element):
        """Click on a payment method"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            
            try:
                element.click()
                return True
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception:
                    try:
                        ActionChains(self.driver).move_to_element(element).click().perform()
                        return True
                    except Exception:
                        return False
        except Exception as e:
            print(f"Error clicking payment method: {e}")
            return False

    def find_any_clickable_button(self):
        """Find specific clickable buttons inside the payment iframe"""
        button_selectors = [
            'button.alerts-ok[onclick="closeForm()"]',
            'button.alerts-ok',
            'div.payment_modal_btn[id="deposit_button"]',
            'div.payment_modal_btn',
            'button[onclick*="closeForm"]',
            'button[onclick*="getForm"]',
            'button.payment_modal_btn[onclick*="getForm"]',
            'button.payment_modal_btn',
            '//button[contains(@class, "alerts-ok")]',
            '//div[contains(@class, "payment_modal_btn")]',
            '//button[contains(@onclick, "closeForm")]',
            '//button[contains(@onclick, "getForm")]',
            '//button[contains(translate(text(), "CONFIRM", "confirm"), "confirm")]',
            '//div[contains(translate(text(), "CONFIRM", "confirm"), "confirm")]',
            '//button[contains(translate(text(), "OK", "ok"), "ok")]',
            '//div[contains(translate(text(), "OK", "ok"), "ok")]',
            '//button[contains(translate(text(), "CONTINUE", "continue"), "continue")]',
            '//div[contains(translate(text(), "CONTINUE", "continue"), "continue")]',
            '//button[contains(translate(text(), "PROCEED", "proceed"), "proceed")]',
            '//div[contains(translate(text(), "PROCEED", "proceed"), "proceed")]',
            '//button[contains(translate(text(), "SUBMIT", "submit"), "submit")]',
            '//div[contains(translate(text(), "SUBMIT", "submit"), "submit")]',
            '//button[contains(translate(text(), "PAY", "pay"), "pay")]',
            '//div[contains(translate(text(), "PAY", "pay"), "pay")]',
            '//button[contains(translate(text(), "DEPOSIT", "deposit"), "deposit")]',
            '//div[contains(translate(text(), "DEPOSIT", "deposit"), "deposit")]',
            '//button[not(contains(translate(text(), "CANCEL", "cancel"), "cancel")) and not(contains(translate(text(), "CLOSE", "close"), "close")) and not(contains(translate(text(), "BACK", "back"), "back")) and not(contains(translate(text(), "EXIT", "exit"), "exit")) and not(contains(@class, "cancel")) and not(contains(@class, "close")) and not(contains(@class, "back"))]',
            '//div[not(contains(translate(text(), "CANCEL", "cancel"), "cancel")) and not(contains(translate(text(), "CLOSE", "close"), "close")) and not(contains(translate(text(), "BACK", "back"), "back")) and not(contains(translate(text(), "EXIT", "exit"), "exit")) and not(contains(@class, "cancel")) and not(contains(@class, "close")) and not(contains(@class, "back")) and (@onclick or contains(@class, "btn") or contains(@class, "button"))]',
        ]
        
        for selector in button_selectors:
            try:
                if selector.startswith("//"):
                    elements = self.driver.find_elements(By.XPATH, selector)
                else:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for el in elements:
                    try:
                        if el.is_displayed() and el.is_enabled():
                            text = el.text.strip() or el.get_attribute('value') or el.get_attribute('onclick') or 'No text'
                            class_name = el.get_attribute('class') or ''
                            tag_name = el.tag_name
                            print(f"Found clickable button: '{text}' | Class: '{class_name}' | Tag: {tag_name} | Selector: {selector}")
                            return el, text
                    except Exception:
                        continue
            except Exception:
                continue
        
        print("No specific payment buttons found in iframe")
        return None, None

    def navigate_with_max_depth(self, max_depth=2):
        """Navigate through pages by clicking buttons with maximum depth limit"""
        current_depth = 0
        clicked_buttons = []
        
        print(f"Starting navigation with max depth: {max_depth}")
        
        while current_depth < max_depth:
            print(f"\n--- Navigation Depth: {current_depth + 1}/{max_depth} ---")
            time.sleep(5)
            
            button, button_text = self.find_any_clickable_button()
            if not button:
                print(f"No more payment buttons found at depth {current_depth + 1} - stopping navigation")
                break
            
            if button_text in clicked_buttons:
                print(f"Button '{button_text}' already clicked - looking for different button")
                try:
                    self.driver.execute_script("arguments[0].style.display = 'none';", button)
                    alt_button, alt_button_text = self.find_any_clickable_button()
                    self.driver.execute_script("arguments[0].style.display = '';", button)
                    
                    if alt_button and alt_button_text != button_text:
                        button, button_text = alt_button, alt_button_text
                    else:
                        print("No alternative button found - stopping navigation")
                        break
                except Exception as e:
                    print(f"Error looking for alternative button: {e}")
                    break
            
            print(f"Attempting to click button: '{button_text}'")
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                time.sleep(2)
                
                clicked = False
                try:
                    button.click()
                    clicked = True
                    print("✓ Clicked button with standard click")
                except Exception:
                    try:
                        self.driver.execute_script("arguments[0].click();", button)
                        clicked = True
                        print("✓ Clicked button with JavaScript click")
                    except Exception:
                        try:
                            ActionChains(self.driver).move_to_element(button).click().perform()
                            clicked = True
                            print("✓ Clicked button with ActionChains")
                        except Exception as e:
                            print(f"⚠️ Failed to click button: {e}")
                
                if not clicked:
                    print("Failed to click button - stopping navigation")
                    break
                
                clicked_buttons.append(button_text)
                current_depth += 1
                
                current_url = self.driver.current_url
                if any(exit_indicator in current_url.lower() for exit_indicator in ['success', 'complete', 'error', 'failed', 'redirect']):
                    print(f"Detected completion page in URL: {current_url}")
                    break
                    
            except Exception as e:
                print(f"❌ Error clicking button at depth {current_depth + 1}: {e}")
                break
        
        print(f"Navigation completed at depth: {current_depth}")
        print(f"Buttons clicked: {clicked_buttons}")
        return current_depth

    # --- Data Extraction Algorithms ---

    def extract_upi_details(self, soup, plain_text):
        """Extract typical VPA or UPI ID identifiers found inside gateways"""
        details = {"upi_id": "", "upi_name": ""}
        upi_pattern = re.compile(r'[a-zA-Z0-9.\-_]+@[a-zA-Z0-9]+')
        found_upis = upi_pattern.findall(plain_text)
        
        if found_upis:
            details["upi_id"] = found_upis[0]

        for label in soup.find_all(string=re.compile(r'UPI ID|VPA|Payee Name|Name', re.IGNORECASE)):
            parent = label.parent
            next_text = parent.get_text() if parent else ""
            cleaned = next_text.replace(label, "").strip(": \n")
            if "ID" in label.upper() and not details["upi_id"]:
                details["upi_id"] = cleaned
            elif "NAME" in label.upper():
                details["upi_name"] = cleaned
        return details

    def validate_upi_details(self, details):
        """Sanitize structural outputs for UPI"""
        return {
            "upi_id": details.get("upi_id", "").strip(),
            "upi_name": details.get("upi_name", "").strip()
        }

    def extract_bank_details(self, soup, plain_text):
        """Parse structured layout elements looking for bank processing credentials"""
        details = {"bank_holder_name": "", "bank_account_number": "", "bank_ifsc_code": "", "bank_name": ""}
        
        ifsc_pattern = re.compile(r'[A-Z]{4}0[A-Z0-9]{6}')
        acc_pattern = re.compile(r'\b\d{9,18}\b')
        
        ifsc_match = ifsc_pattern.search(plain_text)
        if ifsc_match:
            details["bank_ifsc_code"] = ifsc_match.group(0)
            
        acc_matches = acc_pattern.findall(plain_text)
        for match in acc_matches:
            if details["bank_ifsc_code"] and match in details["bank_ifsc_code"]:
                continue
            details["bank_account_number"] = match
            break

        for field in soup.find_all(["span", "div", "td", "label"]):
            text = field.get_text().strip()
            if re.search(r'Beneficiary|Holder|Account Name', text, re.IGNORECASE):
                sibling = field.find_next_sibling()
                if sibling: details["bank_holder_name"] = sibling.get_text().strip()
            elif re.search(r'Bank Name', text, re.IGNORECASE):
                sibling = field.find_next_sibling()
                if sibling: details["bank_name"] = sibling.get_text().strip()

        return details

    def validate_bank_details(self, details):
        """Sanitize bank output details"""
        return {
            "bank_holder_name": details.get("bank_holder_name", "").strip(),
            "bank_account_number": details.get("bank_account_number", "").strip(),
            "bank_ifsc_code": details.get("bank_ifsc_code", "").strip(),
            "bank_name": details.get("bank_name", "").strip()
        }

    def extract_crypto_details(self, soup, plain_text):
        """Extract target chain IDs and transaction addresses"""
        details = {"crypto_id": "", "crypto_value": ""}
        crypto_address_pattern = re.compile(r'\b(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{26,33}|T[A-Za-z1-9]{33})\b')
        match = crypto_address_pattern.search(plain_text)
        if match:
            details["crypto_id"] = match.group(0)

        for label in soup.find_all(text=re.compile(r'Address|Network|Crypto Address', re.IGNORECASE)):
            val = label.find_next()
            if val:
                details["crypto_value"] = val.get_text().strip()
        return details

    def validate_crypto_details(self, details):
        """Enforce strict field checks for Crypto data arrays"""
        return {
            "crypto_id": details.get("crypto_id", "").strip(),
            "crypto_value": details.get("crypto_value", "").strip()
        }

    def extract_reference_urls(self, html_content):
        """Collect deep hyperlinks present within current transaction state"""
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if href.startswith(('http', 'https', '//')):
                urls.append(href)
        return list(set(urls))

    def extract_transaction_details(self, html_content, plain_text, payment_name):
        """Enhanced extraction with validation before saving"""
        transaction_details = {}
        soup = BeautifulSoup(html_content, 'html.parser')
        
        upi_details = self.extract_upi_details(soup, plain_text)
        transaction_details.update(self.validate_upi_details(upi_details))
        
        bank_details = self.extract_bank_details(soup, plain_text)
        transaction_details.update(self.validate_bank_details(bank_details))
        
        crypto_details = self.extract_crypto_details(soup, plain_text)
        transaction_details.update(self.validate_crypto_details(crypto_details))
        
        return transaction_details
        
    def should_save_method_data(self, method_data):
        """Determine if method data has valid transaction details worth saving"""
        transaction_details = method_data.get('transaction_details', {})
        
        upi_id = transaction_details.get