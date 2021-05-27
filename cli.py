#!/usr/bin/env python3
"""
Usage: ./cli.py <image/pdf>

Examples:
./cli.py question.jpg
./cli.py paper1.png paper2.pdf
"""

import sys
from PIL import Image
import pytesseract
from pdfminer.high_level import extract_text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import screw_test


def search_and_print(driver, questions: str):
    line = 1
    answer_found = False

    for i in questions:
        # Links will be unique
        urls = list(dict.fromkeys(screw_test.find_question_urls(driver, i)))
        for question in urls:
            answer = screw_test.find_answer(question)
            if answer is not None:
                print()
                print("{}. Question: {}".format(line, question))
                print("Answer: {}".format(answer))

                if answer_found is False:
                    answer_found = True

            line += 1

    if answer_found is False:
        print()
        print("No answers found lol. RIP")


ARGS = len(sys.argv) - 1
if ARGS == 0:
    print("Usage: ./cli.py <image/pdf>")
    print("$ ./cli.py question.jpg")
    print("$ ./cli.py paper1.png paper2.pdf")
    sys.exit(1)

# Run headless browser
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

for input in range(1, ARGS + 1):
    # Get text from image or pdf
    print()
    question_paper = sys.argv[input]
    if question_paper.endswith(".pdf"):
        print("Extracting text from PDF...")
        text = extract_text(question_paper)
    else:
        print("Extracting text from image...")
        text = pytesseract.image_to_string(Image.open(question_paper))

    if not text:
        continue

    print("Detecting questions...")
    questions = screw_test.detect_questions(text)
    if not questions:
        continue

    print("Searching...")
    search_and_print(driver, questions)

driver.quit()
