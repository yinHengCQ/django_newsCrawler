#coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.touch_actions import TouchActions

def download_by_chrome():
    mobile_emulation = {"deviceName": "iPhone 6"}
    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver.exe",chrome_options=options)

    try:
        driver.get('https://m.taobao.com/#index')
        time.sleep(5)
        TouchActions(driver).tap(driver.find_element_by_xpath('//div[@id="a16224-1"]')).perform()
        time.sleep(5)
        print(driver.page_source)
    except Exception as e:print(e)
    finally:driver.quit()


download_by_chrome()