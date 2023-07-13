"""
PDF to text
step 1: convert PDF to image, the image format can be customized
step 2: convert the image to text by `tesseract` command line
 tesseract -l chi_sim image_1.png  aa_tmp.pdf

pytesseract is the python version
"""

import fitz
pdffile = "aa.pdf"
doc = fitz.open(pdffile)
zoom = 4
mat = fitz.Matrix(zoom, zoom)
count = 0
# Count variable is to get the number of pages in the pdf
for p in doc:
    count += 1
for i in range(count):
    val = f"out/image_{i+1}.png"
    page = doc.load_page(i)
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
    print(f"saved {val}")
doc.close()
