"""
PDF to text

convert PDF to image, the image format can be customized

convert the image to text by `tesseract` command line
 tesseract -l chi_sim image_1.png  aa_tmp.pdf

pytesseract is the python version wrapper
"""

import os
import subprocess
import sys

import fitz


input_pdf_fn = sys.argv[1]  # 'bb.pdf'
output_pdf_fn = sys.argv[2]  # 'bb_out.pdf'
lang = 'chi_sim'  # `tesseract --lang-list`

# tmp dir
output_img_dir = 'out_img'
output_img_prefix = 'img_'
output_pdf_dir = 'out_pdf'
output_pdf_prefix = 'pdf_'


print(f"Make sure dir `{output_img_dir}` and `{output_pdf_dir}` have been created!")
subprocess.run(f"mkdir -p {output_img_dir}".split(' '), capture_output=True)
subprocess.run(f"mkdir -p {output_pdf_dir}".split(' '), capture_output=True)


doc = fitz.open(input_pdf_fn)
zoom = 4
mat = fitz.Matrix(zoom, zoom)

# step-1: PDF to image list
print(f"processing {input_pdf_fn}")
out_list = []
cnt = 0
for page in doc:
    out_fn = f"{output_img_prefix}{cnt+1:02d}.png"
    out_list.append(out_fn)
    fn_path = os.path.join(output_img_dir, out_fn)
    pix = page.get_pixmap(matrix=mat)
    #pix.save(fn_path)
    print(f"saved {fn_path}")
    cnt += 1

doc.close()
print(f"output file list:\n{out_list}")

# step-2: convert to pdf for each image file
# command line to generate PDF list from image files
pdf_out_list = []
for in_fn in out_list:
    out_fn = f"{output_pdf_prefix}{in_fn}"
    in_path = os.path.join(output_img_dir, in_fn)
    out_path = os.path.join(output_pdf_dir, out_fn)
    pdf_out_list.append(out_path + '.pdf')  # with .pdf suffix
    cmd = f"tesseract -l {lang} --psm 11 --oem 1 {in_path} {out_path} PDF"
    print(cmd)
    result = subprocess.run(cmd.split(' '), capture_output=True)
    if not result.stdout:
        print('SUCCESS!')
    else:
        print(repr(result.stdout))

# step-3: merge the list to output PDF file
doc_out = fitz.open()

for fn in pdf_out_list:
    print(f"insert {fn}")
    doc_out.insert_pdf(fitz.open(fn))

doc_out.save(output_pdf_fn)
print(f"saved to {output_pdf_fn}")
