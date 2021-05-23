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

# All question paper links. These are the sites I know so far.
# TODO: Add links
URLS = [
]


# NOTE: This function is not perfect, it returns some non-questions too. It's
# not necessary to fix it but the program will become slightly more efficient
# and accurate if I do so.
def get_questions(paper: str) -> str:
    """
    Return all the questions from the paper
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


if QUESTION_PAPER.endswith(".pdf"):
    pdf_text = extract_text(QUESTION_PAPER)
    questions = get_questions(pdf_text)
else:
    image_text = pytesseract.image_to_string(Image.open(QUESTION_PAPER))
    questions = get_questions(image_text)
