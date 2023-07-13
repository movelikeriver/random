"""
PDF to text PDF

the command line version of `ocrmypdf` is:
ocrmypdf --skip-text -l chi_sim ~/Downloads/raw.pdf /tmp/out.pdf
"""

# import libraries
import os
import ocrmypdf
import pandas as pd
import fitz #!pip install PyMuPDF

# get pdf files
work_dir = './'
file_list = ['aa.pdf']

# PATH = os.getcwd()
# file_list = [f for f in os.listdir(path=PATH) if f.endswith('.pdf') or f.endswith('.PDF')]

'''
main ocr code, which create new pdf file with OCR_ ahead its origin filename, 
and error messege can be find in error_log
'''
# %%time 
error_log = {}
for file in file_list:
    try:
        # result = ocrmypdf.ocr(file, 'OCR_'+file,output_type='pdf',skip_text=True,deskew=True)
    	print(f"{file} done")
    except Exception as e:
        if hasattr(e,'message'):
            error_log[file] = e.message
        else:
            error_log[file] = e
        continue
        
'''
extract OCRed PDF using PyMuPDF and save into a pandas dataframe
'''
ocr_file_list = [f for f in os.listdir(path=work_dir) if f.startswith('OCR_') ]

# PDF extraction
# informations we want to extract
extraction_pdfs = {}

for file in ocr_file_list:
    #save the results
    pages_df = pages_df = pd.DataFrame(columns=['text'])
    # file reader
    doc = fitz.open(file)
    print(dir(doc))
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_text = page.get_text('text')
        print(page_text)
        pages_df = pages_df.append({'text': page_text}, ignore_index=True)
        
        
    extraction_pdfs[file] = pages_df  
