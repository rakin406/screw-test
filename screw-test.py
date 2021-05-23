#!/usr/bin/env python3
"""
Ultra cheating program
"""

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# Simple image to string
print(pytesseract.image_to_string(Image.open("test.png")))
