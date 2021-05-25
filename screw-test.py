#!/usr/bin/env python3
"""
Ultra cheating program I made for my dumb friends.
Usage: ./screw-test.py <image/pdf>
Example: ./screw-test.py question-paper.png
"""

import sys
import requests
from pdfminer.high_level import extract_text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Get image or pdf path
if len(sys.argv) > 1:
    QUESTION_PAPER = sys.argv[1]
else:
    print("Usage: ./screw-test.py <image/pdf>")
    print("Example: ./screw-test.py question-paper.png")
    sys.exit(1)


# NOTE: This function is not perfect, it returns some non-questions too. It's
# not necessary to fix it but the program will become slightly more efficient
# and accurate if I do so.
def detect_questions(paper: str) -> str:
    """
    Return all the detected questions from the paper
    """
    questions = []
    for line in paper.splitlines():
        # If line is JUST number, then don't add it to questions.
        line = line.strip()
        if not line.isdigit():
            # If first letter of the line is a number, it means it's a question.
            # For example, "1. What is physics?"
            # How am I so sure that it's a question? Because of experience.
            if len(line) > 0 and line[0].isdigit():
                questions.append(line)
    return questions


def get_ddg_urls(question: str) -> str:
    """
    Return DuckDuckGo URLs for the search query of the question.
    Supports papacambridge, physicsandmathstutor and xtremepapers.
    """
    query_ques = question.replace(" ", "+")
    urls = [
        "https://duckduckgo.com/?q=papacambridge+{}&t=hc&va=u&ia=web".format(
            query_ques
        ),
        "https://duckduckgo.com/?q=physicsandmathstutor+{}&t=hc&va=u&ia=web".format(
            query_ques
        ),
        "https://duckduckgo.com/?q=xtremepapers+{}&t=hc&va=u&ia=web".format(query_ques),
    ]
    return urls


def find_question_urls(driver, question: str) -> str:
    """
    Return URL of major question websites.
    """
    urls = []
    query_urls = get_ddg_urls(question)

    for query in query_urls:
        driver.get(query)

        # Get all website links
        question_urls = driver.find_elements_by_xpath("//a[@href]")
        for elem in question_urls:
            # Check if link contains the question website domains and if it does,
            # append the URL.
            url = elem.get_attribute("href")
            if (
                "https://pmt.physicsandmathstutor.com" in url
                or "https://pastpapers.papacambridge.com" in url
                or "https://papers.xtremepape.rs" in url
            ):
                if url.endswith(".pdf"):
                    urls.append(url)

    return urls


def find_answer(question_url: str) -> str:
    """
    Return answer link.
    """
    answer_url = None

    # Prepare mark scheme links
    if "https://pmt.physicsandmathstutor.com" in question_url:
        # This is how physicsandmathstutor organizes URL. The question paper
        # has "QP.pdf" at the end and the mark scheme paper has "MS.pdf" at the
        # end. The other parts of both URLs are the same.
        answer_url = question_url.replace("QP.pdf", "MS.pdf")
    else:
        answer_url = question_url.replace("_qp_", "_ms_")

    # Check if URL exists
    if answer_url is not None:
        site = requests.get(answer_url)
        if site.status_code == 200:
            return answer_url

    return answer_url


# Get text from image or pdf
if QUESTION_PAPER.endswith(".pdf"):
    print("Extracting text from PDF...")
    text = extract_text(QUESTION_PAPER)
else:
    print("Extracting text from image...")
    text = pytesseract.image_to_string(Image.open(QUESTION_PAPER))

if not text:
    print("No text found!")
    sys.exit(2)

print("Detecting questions...")
questions = detect_questions(text)
if not questions:
    print("No questions found!")
    sys.exit(3)

# Run headless browser
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

line = 1
answer_found = False
print("Searching...")

for ques in questions:
    # Links will be unique
    urls = list(dict.fromkeys(find_question_urls(driver, ques)))
    for url in urls:
        print()
        print("{}. Question: {}".format(line, url))
        answer = find_answer(url)
        if answer is not None:
            if answer_found is False:
                answer_found = True
            print("Answer: {}".format(answer))
        line += 1

if answer_found is False:
    print()
    print("No answers found lol. RIP")

driver.quit()
