#!/usr/bin/env python3
"""
Ultra cheating program I made for my dumb friends.
Usage: ./screw-test.py <image>
Example: ./screw-test.py question-paper.png
"""

import sys
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Get image path
if len(sys.argv) > 1:
    IMAGE = sys.argv[1]
else:
    print("Provide question paper image, you lowlife cheater!")
    sys.exit(1)

# Simple image to string
print(pytesseract.image_to_string(Image.open(IMAGE)))
