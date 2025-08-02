from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from collections import namedtuple
import time

CaseResult = namedtuple("CaseResult", ["parties", "filing_date", "next_hearing", "pdf_link"])

def fetch_case_details(case_type, case_number, filing_year):
    options = Options()
    # Headless mode disabled
    # options.add_argument("--headless")

    # Stability flags
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # <-- important for M-series
    options.add_argument("--remote-debugging-port=9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 25)

    try:
        # Go directly to case status page
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus/index")

        # Wait for page to load
        time.sleep(6)

        # Select State: Haryana
        Select(wait.until(EC.presence_of_element_located((By.ID, "sess_state_code")))).select_by_visible_text("Haryana")
        time.sleep(1)

        # Select District: Faridabad
        Select(wait.until(EC.presence_of_element_located((By.ID, "sess_dist_code")))).select_by_visible_text("Faridabad")
        time.sleep(1)

        # Select Court Complex: District Court, Faridabad
        Select(wait.until(EC.presence_of_element_located((By.ID, "court_code")))).select_by_visible_text("District Court, Faridabad")
        time.sleep(1)

        # Click on "Case Number" tab (ensure correct section visible)
        wait.until(EC.element_to_be_clickable((By.ID, "tab2"))).click()

        # Select case type
        Select(wait.until(EC.presence_of_element_located((By.ID, "case_type")))).select_by_visible_text(case_type)

        # Fill in case number and year
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(filing_year)

        # CAPTCHA is present – pause for manual solve
        print("\n🛑 CAPTCHA Present!")
        print("👉 Please enter the captcha in the browser and click 'Go'")
        input("✅ Press ENTER here in terminal once you've clicked Go...\n")

        # Wait for result to appear
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "case_details_container")))
        html = driver.page_source

        # Extract data
        parties = driver.find_element(By.XPATH, "//b[contains(text(),'Petitioner')]/following::td[1]").text.strip()
        filing_date = driver.find_element(By.XPATH, "//td[contains(text(),'Filing Date')]/following-sibling::td[1]").text.strip()
        next_hearing = driver.find_element(By.XPATH, "//td[contains(text(),'Next Date')]/following-sibling::td[1]").text.strip()

        try:
            pdf_link = driver.find_element(By.XPATH, "//a[contains(@href, '.pdf')]").get_attribute("href")
        except:
            pdf_link = "No PDF found"

        return CaseResult(parties, filing_date, next_hearing, pdf_link), html

    except Exception as e:
        raise Exception(f"Scraping failed: {e}")

    finally:
        driver.quit()