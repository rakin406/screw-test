#!/usr/bin/env python3
"""
Ultra cheating program I made for my dumb friends.
Usage: ./screw-test.py <image/pdf>
Example: ./screw-test.py question-paper.png
"""

import sys
from pdfminer.high_level import extract_text_to_fp, extract_text

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Get image or pdf path
if len(sys.argv) > 1:
    QUESTION = sys.argv[1]
else:
    print("Provide question paper image or pdf, you lowlife cheater!")
    sys.exit(1)

if QUESTION.endswith(".pdf"):
    print(extract_text(QUESTION))
else:
    print(pytesseract.image_to_string(Image.open(QUESTION)))
