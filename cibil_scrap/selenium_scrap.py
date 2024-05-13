from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from .constants import URL

def find_ele_id(driver,id_str):
    ele = driver.find_element(By.ID, id_str)
    ele.click()
    return ele

def find_ele_tag(driver, id_str,idx=None):
    ele = driver.find_elements(By.TAG_NAME, id_str)[idx]
    ele.click()
    return ele

def find_ele_xpath(driver, id_str):
    ele = driver.find_element(By.XPATH, id_str)
    if not ele.is_displayed():
        actions = ActionChains(driver)
        actions.move_to_element(ele).perform()
    try:
        driver.execute_script(ele.get_attribute("onclick"))
    except:
        ele.click()
    return ele

def download(driver):
    download_link = driver.find_element(
        By.CSS_SELECTOR, "a[href='downloadStatusReport']"
    )
    download_url = download_link.get_attribute("href")
    download_link.click()

def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(URL)
    time.sleep(2)
    return driver
