from selenium import webdriver
import json
import chrome_selenium_updater.selenium_updater as updater
from email_relay.email_client import EmailClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import dotenv
import time
import os

dotenv.load_dotenv()

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

# Opens Main IKEA page
selenium_driver.get("https://www.ikea.com/us/en/")

# Sets the nearest IKEA store to Renton, WA
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

# Sets the Zip Code to 98119
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
time.sleep(0.5)

# Checks availability of each item
for item in items_to_check:
    # Goes to the item listing
    selenium_driver.get(base_url + item)

    # Waits for availability information to load
    found = False

    while not found:
        try:
            time.sleep(5)
            availablity = selenium_driver.find_element(By.CLASS_NAME, "js-delivery-section").find_element(By.CLASS_NAME, "pip-status").get_attribute("class")
            found = True
        except NoSuchElementException:
            time.sleep(0.1)

    # Checks if item is available and stores result
    if "red" in availablity:
        results.append(False)
    else:
        results.append(True)

    # Stores item name and description
    main_name = selenium_driver.find_element(By.CLASS_NAME, "pip-header-section__title--big").text
    description = selenium_driver.find_element(By.CLASS_NAME, "pip-header-section__description-text").text

    names.append(f"{main_name} - {description}")

# Closes driver
selenium_driver.close()

changes = [0]*len(results)

# Generates a list of changes in availability since the last query
if "ikea_inventory.json" not in os.listdir():
    changes = [2]*len(results)
else:
    with open("ikea_inventory.json", "r") as f:
        old_data = json.load(f)
        for i, item in enumerate(items_to_check):
            if item not in old_data["items"]:
                changes[i] = 2
                continue
            if old_data["results"][old_data["items"].index(item)] != results[i]:
                changes[i] = -1 if not results[i] else 1
                continue
            else:
                changes[i] = 0

# Updates the stored JSON file
with open("ikea_inventory.json", "w") as f:
    json.dump({"items": items_to_check, "results": results, "names": names}, f)

if not any(changes):
    exit()

# Creates body of email to send
subject = "IKEA Inventory Update"
body = "Changes:\n"

for i, change in enumerate(changes):
    if change == 2:
        body += f"New Item : {names[i]}\n"
    elif change == -1:
        body += f"Item Unvailable : {names[i]}\n"
    elif change == 1:
        body += f"Item Available : {names[i]}\n"

body += "\n\nAll Items:\n"

for i, item in enumerate(names):
    body += f"{'Available' if results[i] else 'Unavailable'} : {names[i]}\n"

# Creates Email Client Object and sends email request
email_client = EmailClient()
email_client.connect(os.getenv("HOST"), int(os.getenv("PORT")))
email_client.send(os.getenv("EMAIL"), subject, body)
email_client.close()