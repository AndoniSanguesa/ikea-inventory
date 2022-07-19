from selenium import webdriver
import json
import chrome_selenium_updater.selenium_updater as updater
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# TEMPORARY: Using Chrome Beta 104 until version compatible with Selenium is released
options = Options()
options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"

# Keeps the chromedriver up to date
updater.update_chrome_drivers(options=options)

# Songesand Bed Frame, Songesand Night Stand, Songesand Dresser, Janinge Bar Stool, Toolstorp Coffee Table, Finalla Sleeper Sofa, Brimnes TV Unit, ÄPPLARÖ Table, Lagkapten Tabletop, Alex Drawers, Olov Leg
items_to_check = ["s59241069", "70367444", "50366799", "10281354", "00400277", "s89319033", "50337698", "s99325458", "60487017", "60473548", "30264301"]
results = []
names = []
base_url = "https://www.ikea.com/us/en/p/-"

# Creates webdriver Object 
selenium_driver = webdriver.Chrome(chrome_options=options)

selenium_driver.get("https://www.ikea.com/us/en/")

selenium_driver.find_element(By.CLASS_NAME, "delivery-button").click()

found = False

while not found:
    try:
        geo_input = selenium_driver.find_element(By.CLASS_NAME, "geo-ingka-search__input")
        found = True
    except NoSuchElementException:
        time.sleep(0.1)

geo_input.click()
geo_input.send_keys("Renton")
geo_input.send_keys(Keys.ENTER)
time.sleep(0.2)

found = False

while not found:
    try:
        selenium_driver.find_element(By.CLASS_NAME, "store_information__container").find_element(By.CLASS_NAME, "geo-ingka-btn__inner").click()
        found = True

    except NoSuchElementException:
        time.sleep(0.1)

selenium_driver.find_elements(By.CLASS_NAME, "delivery-button")[1].click()

found = False

while not found:
    try:
        delivery_input = selenium_driver.find_element(By.CLASS_NAME, "delivery-modal").find_element(By.TAG_NAME, "input")
        found = True
    except NoSuchElementException:
        time.sleep(0.1)

delivery_input.click()
delivery_input.send_keys("98119")
time.sleep(0.5)
delivery_input.send_keys(Keys.ENTER)


for item in items_to_check:
    selenium_driver.get(base_url + item)

    found = False

    while not found:
        try:
            time.sleep(5)
            availablity = selenium_driver.find_element(By.CLASS_NAME, "js-delivery-section").find_element(By.CLASS_NAME, "pip-status").get_attribute("class")
            found = True
        except NoSuchElementException:
            time.sleep(0.1)

    if "red" in availablity:
        results.append(False)
    else:
        results.append(True)

    main_name = selenium_driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
    description = selenium_driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text

    names.append(f"{main_name} - {description}")

    print(f"{main_name} - {description} : {availablity}")

for i, name in enumerate(names):
    print(f"{name}: {results[i]}")

selenium_driver.close()

while True:
    pass