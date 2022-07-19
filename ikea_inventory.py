from selenium import webdriver
from bs4 import BeautifulSoup
import chrome_selenium_updater.selenium_updater as updater

updater.update_chrome_drivers()

# Songesand Bed Frame, Songesand Night Stand, Songesand Dresser, Janinge Bar Stool, Toolstorp Coffee Table, Finalla Sleeper Sofa, Brimnes TV Unit, ÄPPLARÖ Table, Lagkapten Tabletop, Alex Drawers, Olov Leg
items_to_check = ["s59241069", "70367444", "50366799", "10281354", "00400277", "s89319033", "50337698", "s99325458", "60487017", "60473548", "30264301"]
base_url = "www.ikea.com/us/en/p/-"

selenium_driver = webdriver.Chrome()

for item in items_to_check:
    selenium_driver.get(base_url + item)