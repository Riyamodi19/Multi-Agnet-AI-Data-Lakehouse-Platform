import os
import re
import time
import json
import base64
import urllib.parse
from datetime import datetime, timezone

import cv2
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

BASE_URL = "https://www.10cric247.com/"


class SimplifiedPaymentScraper:
    PAYMENT_CARD_SELECTOR = "[class*='PaymentRouteCardBase_root']"

    PAYMENT_NAME_SELECTORS = [
        "[class*='PaymentRouteCard_name']",
        "[class*='PaymentRouteCardBase_name']",
        "[class*='name']",
    ]

    PAYMENT_IFRAME_SELECTORS = [
        "iframe[name*='payment']",
        "iframe[id*='payment']",
        "iframe[src*='payment']",
        "iframe[src*='paysystem']",
        "iframe[src*='deposit']",
        "iframe[src*='cashier']",
        "iframe#payments_frame",
    ]

    def __init__(
        self,
        headless=False,
        wait_timeout=20,
        max_methods=103,
    ):
        self.wait_timeout = wait_timeout
        self.max_methods = max_methods
        self.base_url = BASE_URL

        self.output_dir = os.path.abspath("OUTPUT_10")
        self.json_dir = os.path.join(self.output_dir, "json")
        self.html_dir = os.path.join(self.output_dir, "html")
        self.qr_dir = os.path.join(self.output_dir, "qr")
        self.screenshot_dir = os.path.join(
            self.output_dir,
            "screenshots",
        )
        self.log_dir = os.path.join(self.output_dir, "logs")

        self.run_id = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.driver = None
        self.wait = None
        self.main_window = None
        self.payment_page_url = None

        self.processed_count = 0
        self.saved_count = 0
        self.failed_count = 0
        self.results = []

        self.setup_directories()
        self.setup_driver(headless)

    # --------------------------------------------------
    # Setup
    # --------------------------------------------------

    def setup_directories(self):
        directories = [
            self.output_dir,
            self.json_dir,
            self.html_dir,
            self.qr_dir,
            self.screenshot_dir,
            self.log_dir,
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        print(f"Output directory: {self.output_dir}")

    def setup_driver(self, headless=False):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            "--disable-dev-shm-usage"
        )
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(
            "--window-size=1920,1080"
        )
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(
            "--disable-blink-features="
            "AutomationControlled"
        )
        chrome_options.add_argument(
            "--disable-extensions"
        )

        chrome_options.page_load_strategy = "eager"

        chrome_options.add_argument(
            "--user-agent="
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=chrome_options,
        )

        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL",
            fix_hairline=True,
        )

        self.wait = WebDriverWait(
            self.driver,
            self.wait_timeout,
        )

        self.main_window = (
            self.driver.current_window_handle
        )

    # --------------------------------------------------
    # Website opening and login
    # --------------------------------------------------

    def wait_for_page_load(self, extra_wait=2):
        try:
            self.wait.until(
                lambda driver: driver.execute_script(
                    "return document.readyState"
                )
                in ("interactive", "complete")
            )
        except TimeoutException:
            print(
                "Page readiness timeout. "
                "Continuing with loaded content."
            )

        time.sleep(extra_wait)

    def open_url_with_retry(
        self,
        url,
        retries=3,
        timeout_seconds=45,
    ):
        self.driver.set_page_load_timeout(
            timeout_seconds
        )

        for attempt in range(1, retries + 1):
            try:
                print(
                    f"Opening {url} "
                    f"(attempt {attempt}/{retries})..."
                )

                self.driver.get(url)
                self.wait_for_page_load(extra_wait=3)

                current_url = (
                    self.driver.current_url or ""
                )

                page_source = (
                    self.driver.page_source or ""
                )

                network_error = (
                    current_url.startswith(
                        "chrome-error://"
                    )
                    or "ERR_CONNECTION_TIMED_OUT"
                    in page_source
                    or "ERR_NAME_NOT_RESOLVED"
                    in page_source
                    or "ERR_CONNECTION_REFUSED"
                    in page_source
                )

                if network_error:
                    raise WebDriverException(
                        "Chrome loaded a network "
                        "error page."
                    )

                print("Website opened successfully.")
                return True

            except TimeoutException:
                print(
                    f"Page timed out on attempt "
                    f"{attempt}/{retries}."
                )

                try:
                    self.driver.execute_script(
                        "window.stop();"
                    )
                except Exception:
                    pass

            except WebDriverException as error:
                message = str(error)

                if (
                    "ERR_CONNECTION_TIMED_OUT"
                    in message
                ):
                    print(
                        "Connection timed out."
                    )

                elif (
                    "ERR_NAME_NOT_RESOLVED"
                    in message
                ):
                    print(
                        "DNS could not resolve "
                        "the website."
                    )
                    return False

                elif (
                    "ERR_CONNECTION_REFUSED"
                    in message
                ):
                    print(
                        "The server refused "
                        "the connection."
                    )

                elif (
                    "ERR_INTERNET_DISCONNECTED"
                    in message
                ):
                    print(
                        "No internet connection."
                    )
                    return False

                else:
                    print(
                        "Chrome network error:",
                        error,
                    )

            if attempt < retries:
                delay = attempt * 5

                print(
                    f"Waiting {delay} seconds "
                    "before retrying..."
                )

                time.sleep(delay)

        return False

    def perform_login(self):
        print("\nManual login mode enabled.")

        opened = self.open_url_with_retry(
            self.base_url,
            retries=3,
            timeout_seconds=45,
        )

        if not opened:
            print(
                "\nThe configured website "
                "could not be reached."
            )

            replacement_url = input(
                "Paste an authorised working URL "
                "or press ENTER to stop: "
            ).strip()

            if not replacement_url:
                return False

            if not replacement_url.startswith(
                ("http://", "https://")
            ):
                replacement_url = (
                    "https://" + replacement_url
                )

            opened = self.open_url_with_retry(
                replacement_url,
                retries=2,
                timeout_seconds=45,
            )

            if not opened:
                print(
                    "The replacement URL "
                    "could not be opened."
                )
                return False

            self.base_url = replacement_url

        print(
            "\nSTEP 1: Log in manually "
            "inside the opened Chrome window."
        )
        print(
            "STEP 2: Complete OTP or CAPTCHA "
            "manually when required."
        )
        print(
            "STEP 3: Open the Deposit/Cashier page."
        )
        print(
            "STEP 4: Make sure payment methods "
            "are visible."
        )
        print(
            "STEP 5: Return to the VS Code terminal."
        )

        input(
            "\nPress ENTER after payment "
            "methods are visible..."
        )

        current_url = self.driver.current_url or ""

        if current_url.startswith(
            "chrome-error://"
        ):
            print(
                "Chrome is still showing "
                "a network error page."
            )
            return False

        self.payment_page_url = current_url

        return True

    # --------------------------------------------------
    # Frame handling
    # --------------------------------------------------

    def switch_to_default_content(self):
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

    def switch_to_payment_iframe(
        self,
        silent=False,
    ):
        self.switch_to_default_content()

        for selector in (
            self.PAYMENT_IFRAME_SELECTORS
        ):
            try:
                frames = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    selector,
                )

                for frame in frames:
                    if not frame.is_displayed():
                        continue

                    self.driver.switch_to.frame(frame)

                    cards = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        self.PAYMENT_CARD_SELECTOR,
                    )

                    if cards:
                        if not silent:
                            print(
                                "Payment iframe found:",
                                selector,
                            )
                        return True

                    self.switch_to_default_content()

            except Exception:
                self.switch_to_default_content()

        self.switch_to_default_content()

        try:
            frames = self.driver.find_elements(
                By.TAG_NAME,
                "iframe",
            )

            for index in range(len(frames)):
                try:
                    self.switch_to_default_content()

                    frames = (
                        self.driver.find_elements(
                            By.TAG_NAME,
                            "iframe",
                        )
                    )

                    if index >= len(frames):
                        break

                    frame = frames[index]

                    if not frame.is_displayed():
                        continue

                    self.driver.switch_to.frame(
                        frame
                    )

                    cards = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        self.PAYMENT_CARD_SELECTOR,
                    )

                    if cards:
                        if not silent:
                            print(
                                "Payment cards found "
                                f"in iframe {index}."
                            )
                        return True

                except Exception:
                    continue

        except Exception:
            pass

        self.switch_to_default_content()
        return False

    def find_payment_context(self):
        self.switch_to_default_content()

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            self.PAYMENT_CARD_SELECTOR,
        )

        if cards:
            return "main"

        if self.switch_to_payment_iframe(
            silent=True
        ):
            return "iframe"

        self.switch_to_default_content()
        return "none"

    # --------------------------------------------------
    # Payment methods
    # --------------------------------------------------

    def extract_payment_methods(self):
        context = self.find_payment_context()

        if context == "none":
            print(
                "Payment cards were not found "
                "in the page or iframe."
            )
            return []

        try:
            elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                self.PAYMENT_CARD_SELECTOR,
            )

            visible_elements = []

            for element in elements:
                try:
                    if element.is_displayed():
                        visible_elements.append(
                            element
                        )
                except (
                    StaleElementReferenceException
                ):
                    continue

            print(
                f"Found {len(visible_elements)} "
                "visible payment methods."
            )

            return visible_elements

        except Exception as error:
            print(
                "Error finding payment methods:",
                error,
            )
            return []

    def extract_payment_name(self, element):
        for selector in (
            self.PAYMENT_NAME_SELECTORS
        ):
            try:
                name_element = (
                    element.find_element(
                        By.CSS_SELECTOR,
                        selector,
                    )
                )

                name = name_element.text.strip()

                if name:
                    return name

            except Exception:
                continue

        try:
            full_text = element.text.strip()

            if full_text:
                return (
                    full_text.splitlines()[0]
                    .strip()
                )

        except Exception:
            pass

        return "Unknown"

    def click_payment_method(self, element):
        try:
            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
                """,
                element,
            )

            time.sleep(1)

            try:
                element.click()
                return True
            except Exception:
                pass

            try:
                self.driver.execute_script(
                    "arguments[0].click();",
                    element,
                )
                return True
            except Exception:
                pass

            try:
                ActionChains(
                    self.driver
                ).move_to_element(
                    element
                ).click().perform()

                return True

            except Exception:
                return False

        except Exception as error:
            print(
                "Payment click error:",
                error,
            )
            return False

    # --------------------------------------------------
    # Window and payment-page handling
    # --------------------------------------------------

    def close_extra_tabs(self):
        handles = self.driver.window_handles

        if not handles:
            return

        main_handle = (
            self.main_window or handles[0]
        )

        for handle in handles:
            if handle == main_handle:
                continue

            try:
                self.driver.switch_to.window(
                    handle
                )
                self.driver.close()
            except Exception:
                pass

        try:
            self.driver.switch_to.window(
                main_handle
            )
        except Exception:
            remaining = (
                self.driver.window_handles
            )

            if remaining:
                self.driver.switch_to.window(
                    remaining[0]
                )
                self.main_window = remaining[0]

    def close_visible_modal(self):
        self.switch_to_default_content()

        selectors = [
            "button[aria-label='Close']",
            "button[aria-label='close']",
            "button[class*='close']",
            "[role='dialog'] button[class*='close']",
            "[data-testid*='close']",
        ]

        for selector in selectors:
            try:
                elements = (
                    self.driver.find_elements(
                        By.CSS_SELECTOR,
                        selector,
                    )
                )

                for element in elements:
                    if not element.is_displayed():
                        continue

                    try:
                        element.click()
                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].click();",
                            element,
                        )

                    time.sleep(1)
                    return True

            except Exception:
                continue

        return False

    def return_to_payment_list(self):
        self.close_extra_tabs()
        self.switch_to_default_content()
        self.close_visible_modal()

        cards = self.extract_payment_methods()

        if cards:
            return True

        if self.payment_page_url:
            try:
                print(
                    "Returning to saved "
                    "payment-page URL..."
                )

                self.driver.get(
                    self.payment_page_url
                )
                self.wait_for_page_load()

                cards = (
                    self.extract_payment_methods()
                )

                if cards:
                    return True

            except Exception as error:
                print(
                    "Could not reopen "
                    "payment page:",
                    error,
                )

        print(
            "\nPlease manually reopen "
            "the Deposit/Cashier page."
        )

        input(
            "Press ENTER when payment "
            "methods are visible..."
        )

        self.payment_page_url = (
            self.driver.current_url
        )

        return bool(
            self.extract_payment_methods()
        )

    def wait_for_payment_context(
        self,
        old_handles,
    ):
        time.sleep(3)

        new_handles = [
            handle
            for handle
            in self.driver.window_handles
            if handle not in old_handles
        ]

        if new_handles:
            self.driver.switch_to.window(
                new_handles[-1]
            )

            self.wait_for_page_load()

            print(
                "Payment method opened "
                "in a new tab."
            )

            return "new_tab"

        self.switch_to_default_content()

        modal_selectors = [
            "[role='dialog']",
            "[class*='modal']",
            "[class*='Modal']",
            "[class*='popup']",
            "[class*='Popup']",
        ]

        for selector in modal_selectors:
            try:
                elements = (
                    self.driver.find_elements(
                        By.CSS_SELECTOR,
                        selector,
                    )
                )

                if any(
                    element.is_displayed()
                    for element in elements
                ):
                    print(
                        "Payment method opened "
                        "in a modal."
                    )
                    return "modal"

            except Exception:
                continue

        iframes = self.driver.find_elements(
            By.TAG_NAME,
            "iframe",
        )

        if iframes:
            print(
                f"Payment context contains "
                f"{len(iframes)} iframe(s)."
            )
            return "iframe"

        return "same_page"

    # --------------------------------------------------
    # QR decoding using OpenCV
    # --------------------------------------------------

    def extract_qr_details(self, qr_file):
        try:
            image = cv2.imread(qr_file)

            if image is None:
                print(
                    "QR image could not be opened:",
                    qr_file,
                )
                return {}

            detector = cv2.QRCodeDetector()

            qr_data, points, _ = (
                detector.detectAndDecode(image)
            )

            if not qr_data:
                print("QR was not decoded.")
                return {}

            qr_data = qr_data.strip()

            print("QR decoded successfully.")

            if not qr_data.lower().startswith(
                "upi://"
            ):
                return {
                    "crypto_token": qr_data
                }

            parsed = urllib.parse.urlparse(
                qr_data
            )

            parameters = (
                urllib.parse.parse_qs(
                    parsed.query
                )
            )

            return {
                "upi_id": parameters.get(
                    "pa",
                    [""],
                )[0],
                "upi_name": parameters.get(
                    "pn",
                    [""],
                )[0],
                "amount": parameters.get(
                    "am",
                    [""],
                )[0],
                "transaction_reference":
                    parameters.get(
                        "tr",
                        [""],
                    )[0],
                "currency": parameters.get(
                    "cu",
                    [""],
                )[0],
                "note": parameters.get(
                    "tn",
                    [""],
                )[0],
            }

        except Exception as error:
            print(
                "QR decoding error:",
                error,
            )
            return {}

    def save_base64_image(
        self,
        source,
        filename,
    ):
        if not source.startswith(
            "data:image"
        ):
            return None

        try:
            _, encoded_data = source.split(
                ",",
                1,
            )

            file_path = os.path.join(
                self.qr_dir,
                filename,
            )

            with open(
                file_path,
                "wb",
            ) as file:
                file.write(
                    base64.b64decode(
                        encoded_data
                    )
                )

            return file_path

        except Exception as error:
            print(
                "Base64 image save error:",
                error,
            )
            return None

    def extract_qr_from_html(
        self,
        html_content,
        method_index,
    ):
        soup = BeautifulSoup(
            html_content,
            "html.parser",
        )

        images = soup.find_all("img")

        print(
            f"Images found: {len(images)}"
        )

        for image_index, image in enumerate(
            images
        ):
            source = image.get("src", "")

            if not source.startswith(
                "data:image"
            ):
                continue

            filename = (
                f"method_{method_index}_"
                f"image_{image_index}.png"
            )

            image_path = self.save_base64_image(
                source,
                filename,
            )

            if not image_path:
                continue

            details = self.extract_qr_details(
                image_path
            )

            if details:
                return details

        return {}

    def extract_qr_from_canvas(
        self,
        method_index,
    ):
        try:
            canvases = self.driver.find_elements(
                By.TAG_NAME,
                "canvas",
            )
        except Exception:
            return {}

        print(
            f"Canvas elements found: "
            f"{len(canvases)}"
        )

        for canvas_index, canvas in enumerate(
            canvases
        ):
            try:
                canvas_data = (
                    self.driver.execute_script(
                        """
                        return arguments[0]
                            .toDataURL('image/png');
                        """,
                        canvas,
                    )
                )

                if (
                    not canvas_data
                    or "," not in canvas_data
                ):
                    continue

                _, encoded_data = (
                    canvas_data.split(",", 1)
                )

                filename = (
                    f"method_{method_index}_"
                    f"canvas_{canvas_index}.png"
                )

                file_path = os.path.join(
                    self.qr_dir,
                    filename,
                )

                with open(
                    file_path,
                    "wb",
                ) as file:
                    file.write(
                        base64.b64decode(
                            encoded_data
                        )
                    )

                details = (
                    self.extract_qr_details(
                        file_path
                    )
                )

                if details:
                    return details

            except Exception as error:
                print(
                    f"Canvas {canvas_index} "
                    f"error:",
                    error,
                )

        return {}

    # --------------------------------------------------
    # Text and transaction extraction
    # --------------------------------------------------

    def extract_plain_text(self, html):
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        collected_texts = []

        visible_text = soup.get_text(
            separator="\n",
            strip=True,
        )

        if visible_text:
            collected_texts.append(
                visible_text
            )

        useful_attributes = {
            "value",
            "alt",
            "title",
            "aria-label",
            "placeholder",
        }

        for element in soup.find_all(True):
            for attribute, value in (
                element.attrs.items()
            ):
                if isinstance(
                    value,
                    (list, tuple),
                ):
                    value = " ".join(value)

                if not value:
                    continue

                if (
                    attribute
                    in useful_attributes
                    or attribute.startswith(
                        "data-"
                    )
                ):
                    collected_texts.append(
                        str(value).strip()
                    )

        plain_text = "\n".join(
            collected_texts
        )

        plain_text = re.sub(
            r"\n\s*\n+",
            "\n\n",
            plain_text,
        )

        return "\n".join(
            line.strip()
            for line in plain_text.splitlines()
            if line.strip()
        )

    def extract_upi_details(
        self,
        plain_text,
    ):
        details = {
            "upi_id": "",
            "upi_name": "",
        }

        pattern = re.compile(
            r"\b[A-Za-z0-9._-]+@"
            r"[A-Za-z0-9._-]+\b"
        )

        matches = pattern.findall(
            plain_text
        )

        filtered = [
            value
            for value in matches
            if not value.lower().endswith(
                (
                    ".com",
                    ".org",
                    ".net",
                    ".in",
                    ".io",
                )
            )
        ]

        if filtered:
            details["upi_id"] = filtered[0]

        return details

    def extract_bank_details(
        self,
        plain_text,
    ):
        details = {
            "bank_holder_name": "",
            "bank_account_number": "",
            "bank_ifsc_code": "",
            "bank_name": "",
        }

        ifsc_pattern = re.compile(
            r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
        )

        account_pattern = re.compile(
            r"\b\d{9,18}\b"
        )

        ifsc_match = ifsc_pattern.search(
            plain_text.upper()
        )

        if ifsc_match:
            details["bank_ifsc_code"] = (
                ifsc_match.group(0)
            )

        account_matches = (
            account_pattern.findall(
                plain_text
            )
        )

        if account_matches:
            details[
                "bank_account_number"
            ] = account_matches[0]

        return details

    def extract_crypto_details(
        self,
        plain_text,
    ):
        details = {
            "crypto_id": "",
            "crypto_coin": "",
            "crypto_network": "",
            "crypto_token": "",
        }

        address_patterns = [
            r"\b0x[a-fA-F0-9]{40}\b",
            (
                r"\b[13]"
                r"[a-km-zA-HJ-NP-Z1-9]"
                r"{25,34}\b"
            ),
            r"\bbc1[a-zA-HJ-NP-Z0-9]{25,90}\b",
            r"\bT[A-Za-z1-9]{33}\b",
        ]

        for pattern in address_patterns:
            match = re.search(
                pattern,
                plain_text,
            )

            if match:
                details["crypto_id"] = (
                    match.group(0)
                )
                break

        coin_patterns = {
            "BTC": r"\bBTC\b|\bBitcoin\b",
            "ETH": r"\bETH\b|\bEthereum\b",
            "LTC": r"\bLTC\b|\bLitecoin\b",
            "USDT": r"\bUSDT\b|\bTether\b",
            "TRX": r"\bTRX\b|\bTron\b",
        }

        for coin, pattern in (
            coin_patterns.items()
        ):
            if re.search(
                pattern,
                plain_text,
                re.IGNORECASE,
            ):
                details["crypto_coin"] = coin
                break

        networks = [
            "ERC20",
            "TRC20",
            "BEP20",
            "Bitcoin",
            "Ethereum",
            "Tron",
            "Litecoin",
        ]

        for network in networks:
            if (
                network.lower()
                in plain_text.lower()
            ):
                details[
                    "crypto_network"
                ] = network
                break

        return details

    def extract_transaction_details(
        self,
        html_content,
        plain_text,
    ):
        details = {
            "upi_id": "",
            "upi_name": "",
            "bank_holder_name": "",
            "bank_account_number": "",
            "bank_ifsc_code": "",
            "bank_name": "",
            "crypto_id": "",
            "crypto_coin": "",
            "crypto_network": "",
            "crypto_token": "",
            "amount": "",
            "currency": "",
            "transaction_reference": "",
            "note": "",
        }

        details.update(
            self.extract_upi_details(
                plain_text
            )
        )

        details.update(
            self.extract_bank_details(
                plain_text
            )
        )

        details.update(
            self.extract_crypto_details(
                plain_text
            )
        )

        return details

    def merge_details(
        self,
        original,
        additional,
    ):
        merged = dict(original)

        for key, value in (
            additional.items()
        ):
            if value and not merged.get(key):
                merged[key] = value

        return merged

    # --------------------------------------------------
    # File saving
    # --------------------------------------------------

    def safe_filename(self, value):
        cleaned = re.sub(
            r"[^\w\-.]+",
            "_",
            value.strip(),
        )

        return cleaned[:100] or "unknown"

    def save_html(
        self,
        payment_name,
        html_content,
        suffix="",
    ):
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = (
            f"{self.safe_filename(payment_name)}"
            f"{suffix}_{timestamp}.html"
        )

        file_path = os.path.join(
            self.html_dir,
            filename,
        )

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(html_content)

            return file_path

        except Exception as error:
            print(
                "HTML save error:",
                error,
            )
            return None

    def take_screenshot(
        self,
        payment_name,
    ):
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = (
            f"{self.safe_filename(payment_name)}"
            f"_{timestamp}.png"
        )

        file_path = os.path.join(
            self.screenshot_dir,
            filename,
        )

        try:
            if self.driver.save_screenshot(
                file_path
            ):
                return file_path

        except Exception as error:
            print(
                "Screenshot error:",
                error,
            )

        return None

    def save_method_data(
        self,
        method_data,
    ):
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = (
            "payment_"
            f"{self.safe_filename(
                method_data.get(
                    'payment_method',
                    'unknown',
                )
            )}_"
            f"{timestamp}.json"
        )

        file_path = os.path.join(
            self.json_dir,
            filename,
        )

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    method_data,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            print("JSON saved:", file_path)
            return file_path

        except Exception as error:
            print(
                "JSON save error:",
                error,
            )
            return None

    def save_run_summary(self):
        summary = {
            "run_id": self.run_id,
            "site_name": "10Cric",
            "base_url": self.base_url,
            "payment_page_url":
                self.payment_page_url,
            "processed": self.processed_count,
            "saved": self.saved_count,
            "failed": self.failed_count,
            "completed_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "results": self.results,
        }

        file_path = os.path.join(
            self.log_dir,
            f"run_summary_{self.run_id}.json",
        )

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    summary,
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            print(
                "Run summary saved:",
                file_path,
            )

        except Exception as error:
            print(
                "Summary save error:",
                error,
            )

    # --------------------------------------------------
    # Iframe inspection
    # --------------------------------------------------

    def inspect_iframes(
        self,
        payment_name,
        method_index,
    ):
        results = []

        self.switch_to_default_content()

        try:
            total_frames = len(
                self.driver.find_elements(
                    By.TAG_NAME,
                    "iframe",
                )
            )
        except Exception:
            return results

        print(
            f"Iframes found: {total_frames}"
        )

        for frame_index in range(
            total_frames
        ):
            try:
                self.switch_to_default_content()

                frames = self.driver.find_elements(
                    By.TAG_NAME,
                    "iframe",
                )

                if frame_index >= len(frames):
                    break

                frame = frames[frame_index]

                frame_src = (
                    frame.get_attribute("src")
                    or ""
                )

                frame_id = (
                    frame.get_attribute("id")
                    or ""
                )

                frame_name = (
                    frame.get_attribute("name")
                    or ""
                )

                self.driver.switch_to.frame(
                    frame
                )

                time.sleep(1)

                html_content = (
                    self.driver.page_source
                )

                plain_text = (
                    self.extract_plain_text(
                        html_content
                    )
                )

                details = (
                    self.extract_transaction_details(
                        html_content,
                        plain_text,
                    )
                )

                qr_details = (
                    self.extract_qr_from_html(
                        html_content,
                        method_index,
                    )
                )

                if not qr_details:
                    qr_details = (
                        self.extract_qr_from_canvas(
                            method_index
                        )
                    )

                details = self.merge_details(
                    details,
                    qr_details,
                )

                html_path = self.save_html(
                    payment_name,
                    html_content,
                    f"_iframe_{frame_index}",
                )

                results.append(
                    {
                        "frame_index": frame_index,
                        "frame_src": frame_src,
                        "frame_id": frame_id,
                        "frame_name": frame_name,
                        "html_path": html_path,
                        "plain_text": plain_text,
                        "transaction_details":
                            details,
                    }
                )

            except (
                StaleElementReferenceException
            ):
                print(
                    f"Iframe {frame_index} "
                    "became stale."
                )

            except Exception as error:
                print(
                    f"Iframe {frame_index} "
                    f"error:",
                    error,
                )

        self.switch_to_default_content()

        return results

    # --------------------------------------------------
    # Process one payment method
    # --------------------------------------------------

    def process_payment_method(
        self,
        method_index,
        total_methods,
    ):
        if not self.return_to_payment_list():
            raise RuntimeError(
                "Could not return to "
                "the payment-method list."
            )

        payment_elements = (
            self.extract_payment_methods()
        )

        zero_based_index = method_index - 1

        if zero_based_index >= len(
            payment_elements
        ):
            raise IndexError(
                f"Method {method_index} "
                "is no longer available."
            )

        element = payment_elements[
            zero_based_index
        ]

        payment_name = (
            self.extract_payment_name(
                element
            )
        )

        print("\n" + "=" * 65)
        print(
            f"Processing method "
            f"{method_index}/{total_methods}: "
            f"{payment_name}"
        )
        print("=" * 65)

        old_handles = list(
            self.driver.window_handles
        )

        clicked = self.click_payment_method(
            element
        )

        if not clicked:
            raise RuntimeError(
                f"Could not click "
                f"{payment_name}"
            )

        context_type = (
            self.wait_for_payment_context(
                old_handles
            )
        )

        time.sleep(3)

        screenshot_path = (
            self.take_screenshot(
                payment_name
            )
        )

        html_content = (
            self.driver.page_source
        )

        plain_text = (
            self.extract_plain_text(
                html_content
            )
        )

        transaction_details = (
            self.extract_transaction_details(
                html_content,
                plain_text,
            )
        )

        qr_details = (
            self.extract_qr_from_html(
                html_content,
                method_index,
            )
        )

        if not qr_details:
            qr_details = (
                self.extract_qr_from_canvas(
                    method_index
                )
            )

        transaction_details = (
            self.merge_details(
                transaction_details,
                qr_details,
            )
        )

        html_path = self.save_html(
            payment_name,
            html_content,
            "_main",
        )

        iframe_results = (
            self.inspect_iframes(
                payment_name,
                method_index,
            )
        )

        for frame_result in iframe_results:
            frame_details = frame_result.get(
                "transaction_details",
                {},
            )

            transaction_details = (
                self.merge_details(
                    transaction_details,
                    frame_details,
                )
            )

        method_data = {
            "record_id": (
                f"10cric_{self.run_id}_"
                f"{method_index}"
            ),
            "site_name": "10Cric",
            "payment_method_index":
                method_index,
            "payment_method":
                payment_name,
            "context_type":
                context_type,
            "page_url":
                self.driver.current_url,
            "payment_page_url":
                self.payment_page_url,
            "transaction_details":
                transaction_details,
            "plain_text":
                plain_text,
            "main_html_path":
                html_path,
            "iframe_results":
                iframe_results,
            "screenshot_path":
                screenshot_path,
            "fetch_time":
                datetime.now(
                    timezone.utc
                ).isoformat(),
            "status":
                "processed",
        }

        json_path = self.save_method_data(
            method_data
        )

        if json_path:
            method_data["json_path"] = (
                json_path
            )
            method_data["status"] = "saved"
            self.saved_count += 1

        return method_data

    # --------------------------------------------------
    # Main method
    # --------------------------------------------------

    def run_scraper_enhanced(self):
        try:
            print(
                "\nStarting Enhanced "
                "10Cric Payment Scraper"
            )
            print(
                "Target URL:",
                self.base_url,
            )
            print(
                "Run ID:",
                self.run_id,
            )

            if not self.perform_login():
                print(
                    "Unable to open or "
                    "log in to the website."
                )
                return

            self.wait_for_page_load()

            self.payment_page_url = (
                self.driver.current_url
            )

            payment_elements = (
                self.extract_payment_methods()
            )

            if not payment_elements:
                print(
                    "\nNo payment methods found."
                )
                print(
                    "Make sure the payment cards "
                    "are visible before pressing ENTER."
                )
                return

            total_methods = min(
                len(payment_elements),
                self.max_methods,
            )

            print(
                f"\nTotal methods to process: "
                f"{total_methods}"
            )

            start_value = input(
                "Enter starting method number "
                "or press ENTER for 1: "
            ).strip()

            try:
                start_index = (
                    int(start_value)
                    if start_value
                    else 1
                )
            except ValueError:
                start_index = 1

            if start_index < 1:
                start_index = 1

            if start_index > total_methods:
                print(
                    "Starting method number "
                    "is too large."
                )
                return

            for method_index in range(
                start_index,
                total_methods + 1,
            ):
                self.processed_count += 1

                try:
                    result = (
                        self.process_payment_method(
                            method_index,
                            total_methods,
                        )
                    )

                    self.results.append(
                        {
                            "payment_method_index":
                                method_index,
                            "payment_method":
                                result.get(
                                    "payment_method"
                                ),
                            "status":
                                result.get(
                                    "status"
                                ),
                            "json_path":
                                result.get(
                                    "json_path"
                                ),
                        }
                    )

                except KeyboardInterrupt:
                    print(
                        "\nScraping stopped "
                        "by the user."
                    )
                    break

                except Exception as error:
                    self.failed_count += 1

                    print(
                        f"Method {method_index} "
                        f"failed:",
                        error,
                    )

                    self.results.append(
                        {
                            "payment_method_index":
                                method_index,
                            "status":
                                "failed",
                            "error":
                                str(error),
                            "timestamp":
                                datetime.now(
                                    timezone.utc
                                ).isoformat(),
                        }
                    )

                finally:
                    try:
                        self.close_extra_tabs()
                        self.switch_to_default_content()
                    except Exception:
                        pass

            print("\n" + "-" * 65)
            print("SCRAPING FINISHED")
            print(
                "Processed:",
                self.processed_count,
            )
            print(
                "Saved:",
                self.saved_count,
            )
            print(
                "Failed:",
                self.failed_count,
            )
            print("-" * 65)

        except KeyboardInterrupt:
            print(
                "\nProgram stopped by user."
            )

        except Exception as error:
            print(
                "\nGlobal scraper error:",
                error,
            )

        finally:
            self.save_run_summary()

            if self.driver:
                print(
                    "Closing Chrome driver..."
                )

                try:
                    self.driver.quit()
                except Exception:
                    pass


if __name__ == "__main__":
    scraper = SimplifiedPaymentScraper(
        headless=False,
        wait_timeout=20,
        max_methods=103,
    )

    scraper.run_scraper_enhanced()