from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# -------------------------
# Setup Selenium WebDriver
# -------------------------
options = Options()
options.add_argument("--headless")  # Run in background without opening a browser window
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# ------------------------------
# Load the Alibaba RFQ page URL
# ------------------------------
url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y"
driver.get(url)
time.sleep(5)  # Wait for content to fully load

# ------------------------------
# Initialize results container
# ------------------------------
data = []

# ------------------------------
# Loop through multiple pages
# ------------------------------
while True:
    # Locate all RFQ listing containers
    rfq_cards = driver.find_elements(By.CLASS_NAME, "brh-rfq-item")

    for card in rfq_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "brh-rfq-item__subject-link").text.strip()
        except:
            title = 'N/A'

        try:
            desc = card.find_element(By.CLASS_NAME, "brh-rfq-item__detail").text.strip()
        except:
            desc = 'N/A'

        try:
            quantity = card.find_element(By.CLASS_NAME, "brh-rfq-item__quantity-num").text.strip()
        except:
            quantity = 'N/A'

        try:
            country = card.find_element(By.CSS_SELECTOR, ".brh-rfq-item__country-flag").get_attribute("title").strip()
        except:
            country = 'N/A'

        try:
            buyer = card.find_element(By.CLASS_NAME, "text").text.strip()
        except:
            buyer = 'N/A'

        try:
            posted = card.find_element(By.CLASS_NAME, "brh-rfq-item__publishtime").text.strip().split("\n")[-1]
        except:
            posted = 'N/A'

        try:
            quotes = card.find_element(By.CSS_SELECTOR, ".brh-rfq-item__quote-left span").text.strip()
        except:
            quotes = 'N/A'

        # Clean data without embedded labels
        data.append({
            'Title': title,
            'Description': desc,
            'Quantity': quantity,
            'Country': country,
            'Buyer Name': buyer,
            'Posted Time': posted,
            'Quotes Left': quotes
        })

    try:
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next') or contains(@class,'next-btn')]")
        if 'disabled' in next_btn.get_attribute('class'):
            break
        next_btn.click()
        time.sleep(5)
    except NoSuchElementException:
        break

# -------------------------
# Save data in formatted text style to CSV
# -------------------------
with open("output.csv", "w", encoding='utf-8') as f:
    for item in data:
        for key, value in item.items():
            # Clean the value by removing extra newlines and spaces
            clean_value = str(value).replace('\n', ' ').replace('\r', ' ').strip()
            f.write(f"{key}: {clean_value}\n")
        f.write("\n")  # Add blank line between entries

# -------------------------
# Clean up
# -------------------------
driver.quit()
print("Scraping completed. Results saved to output.csv")