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
from selenium.webdriver.firefox.options import Options
import screw_test


def rchop(s, suffix) -> str:
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


ARGS = len(sys.argv) - 1
if ARGS == 0:
    print("Usage: ./bot.py <instagram>")
    sys.exit(1)

profile = webdriver.FirefoxProfile(get_profile_path())
driver = webdriver.Firefox(profile)
driver.get("https://www.instagram.com/direct/inbox/")
