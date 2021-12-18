from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
import sys

url_portfolio = "https://www.masterworks.io/dashboard/portfolio"

email = sys.argv[1]
password = sys.argv[2]


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver


def sign_in(email, password, driver):
    url = "https://masterworks.io"
    driver.get(url)
    time.sleep(20)
    sign_in = driver.find_element_by_css_selector(
        '[class="kHZaNF0Q m5tNBq4X _xZgNuHy qVA5xAXM _HuCtb1G"]'
    )
    sign_in.click()
    email_input = driver.find_element_by_css_selector('[aria-label="Email address"]')
    email_input.clear()
    email_input.send_keys(email)
    password_input = driver.find_element_by_css_selector('[aria-label="Password"]')
    password_input.clear()
    password_input.send_keys(password)
    sign_in = driver.find_element_by_css_selector('[value="Sign in"]')
    sign_in.click()
    time.sleep(5)
    logged_in_driver = driver
    return logged_in_driver


def get_portfolio(driver):
    driver.get(url_portfolio)
    time.sleep(10)
    html = driver.page_source
    df = pd.read_html(html)[0]
    df = df.loc[df["Investment Name"] != "Total"]
    df.drop(columns=["Unnamed: 0"], inplace=True)
    df.columns = df.columns.str.replace(" ", "_", regex=False)
    df.columns = map(str.lower, df.columns)
    for col in df.columns:
        try:
            df[col] = df[col].str.replace("$", "", regex=False)
            df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = df[col].str.replace("*", "", regex=False)
            df[col] = df[col].str.replace("—", "0", regex=False)
        except:
            pass  # not a string column
    return df


def main(email, password):
    driver = get_driver()
    driver = sign_in(email, password, driver)
    portfolio = get_portfolio(driver)
    driver.close()
    driver.quit()
    return portfolio


if __name__ == "__main__":
    main(email, password)
