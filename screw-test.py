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
        line = line.strip()

        # If line is JUST number, then don't add it to questions.
        if not line.isdigit():
            # If first letter of the line is a number, it means it's a question.
            # For example, "1. What is physics?"
            # How am I so sure that it's a question? Because of experience.
            if len(line) > 0 and line[0].isdigit():
                questions.append(line)
    return questions


# TODO: Don't support JUST physicsandmathstutor but also many others.
def find_question_url(question: str) -> str:
    """
    Return URL of major mark scheme websites.
    """
    urls = []

    # Create duckduckgo-searchable URL. The reason I chose duckduckgo instead
    # of google is because scraping google is harder(they do not show the full
    # URL of the links).
    search_url = "https://duckduckgo.com/?q=physicsandmathstutor+"

    # Search query
    for word in question.split():
        search_url += word
        search_url += "+"

    page = requests.get(search_url)
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


if QUESTION_PAPER.endswith(".pdf"):
    pdf_text = extract_text(QUESTION_PAPER)
    questions = detect_questions(pdf_text)

    # Test
    for ques in questions:
        urls = find_question_url(ques)
        for url in urls:
            print(url)
else:
    image_text = pytesseract.image_to_string(Image.open(QUESTION_PAPER))
    questions = detect_questions(image_text)
    for ques in questions:
        urls = find_question_url(ques)
        for url in urls:
            print(url)
