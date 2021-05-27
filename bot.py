#!/usr/bin/env python3
"""
This program will send mark schemes automatically to your friends.
Usage: ./bot.py <instagram>
"""

import sys
from PIL import Image
import pytesseract
from pdfminer.high_level import extract_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import screw_test


def rchop(s: str, suffix: str) -> str:
    """
    Remove last occurence of the substring.
    """
    if suffix and s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def get_profile_path() -> str:
    """
    Get current Firefox profile path.
    """
    # Run headless browser
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get("about:profiles")
    profile = driver.find_elements_by_tag_name("td")[1].text
    profile = rchop(profile, "Open Directory")
    driver.quit()
    return profile


def text_person(text: str):
    """
    Text the person on instagram
    """
    input_area = driver.find_element_by_tag_name("textarea")
    input_area.send_keys(
        'Hello there. This program is written by Rakin. You can start using me by saying "start".'
    )
    input_area.send_keys(Keys.RETURN)


ARGS = len(sys.argv) - 1
if ARGS == 0:
    print("Usage: ./bot.py <instagram>")
    sys.exit(1)

profile = webdriver.FirefoxProfile(get_profile_path())
driver = webdriver.Firefox(profile)

# Find the person
driver.get("https://www.instagram.com/direct/inbox/")
try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), '{}')]".format(sys.argv[1]))
        )
    )
except:
    print("Usage: ./bot.py <instagram>")
    sys.exit(2)

username.click()

# Text the person
input_area = driver.find_element_by_tag_name("textarea")
input_area.send_keys(
    'Hello there. This program is written by Rakin. You can start using me by saying "start".'
)
input_area.send_keys(Keys.RETURN)
