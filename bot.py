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


def find_person(driver, username: str):
    """
    Find and click the person.
    """
    try:
        person = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), '{}')]".format(sys.argv[1]))
            )
        )
    except:
        print("Your internet connection is too slow.")
        sys.exit(1)

    person.click()


def text_person(driver, text: str):
    """
    Text the person on instagram.
    """
    input_area = driver.find_element_by_tag_name("textarea")
    input_area.send_keys(text)
    input_area.send_keys(Keys.RETURN)


def get_message(driver) -> str:
    """
    Get the person's last message.
    """
    message = driver.find_elements_by_tag_name("span")[-2].text
    return message


ARGS = len(sys.argv) - 1
if ARGS == 0:
    print("Usage: ./bot.py <instagram>")
    sys.exit(1)

profile = webdriver.FirefoxProfile(get_profile_path())
driver = webdriver.Firefox(profile)

driver.get("https://www.instagram.com/direct/inbox/")
find_person(driver, sys.argv[1])
text_person(
    driver,
    'Hello there. This program is written by Rakin. You can start using me by saying "start".',
)
print(get_message(driver))
