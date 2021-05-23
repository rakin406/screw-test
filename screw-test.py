#!/usr/bin/env python3
"""
Ultra cheating program I made for my dumb friends.
Usage: ./screw-test.py <image/pdf>
Example: ./screw-test.py question-paper.png
"""

import sys
from pdfminer.high_level import extract_text
import requests
from bs4 import BeautifulSoup

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


# TODO: Don't support JUST physicsandmathstutor but also many others.
def get_ddg_url(question: str) -> str:
    """
    Return DuckDuckGo URL for the search query of the question.
    """
    # The reason I chose duckduckgo instead of google is because scraping
    # google is harder(they do not show the full URL of the links).
    url = "https://duckduckgo.com/?q=physicsandmathstutor+"

    # Search query
    words = question.split()
    for word in words:
        url += word
        if word == words[-1]:
            # I don't know if this is needed.
            url += "&t=hc&va=u&ia=web"
        else:
            url += "+"

    return url


# TODO: Don't support JUST physicsandmathstutor but also many others.
def find_question_urls(question: str) -> str:
    """
    Return URL of major mark scheme websites.
    """
    urls = []
    page = requests.get(get_ddg_url(question))
    soup = BeautifulSoup(page.content, "lxml")

    # Get all website links
    a_tags = soup.find_all("a")
    for content in a_tags:
        # Check if link contains the domain "pmt.physicsandmathstutor.com" and
        # if it does, append the URL.
        domain_url = content.find("span", class_="result__url__domain")
        if domain_url.text == "https://pmt.physicsandmathstutor.com":
            end_url = content.find("span", class_="result__url__full")
            question_url = domain_url.text + end_url.text
            urls.append(question_url)

    return urls


# Get text from image or pdf
if QUESTION_PAPER.endswith(".pdf"):
    print("Extracting text from PDF...")
    text = extract_text(QUESTION_PAPER)
else:
    print("Extracting text from image...")
    text = pytesseract.image_to_string(Image.open(QUESTION_PAPER))

print("Detecting questions...")
questions = detect_questions(text)

# Test
for ques in questions:
    urls = find_question_urls(ques)
    for url in urls:
        print(url)
