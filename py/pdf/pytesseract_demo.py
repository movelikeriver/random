"""
PDF to text PDF

pytesseract is the python version of `tesseract`
 
tesseract -l chi_sim image_1.png  aa_tmp.pdf

"""

# import libs
try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import pytesseract
import os
import numpy as np
import pandas as pd
import re
from pdf2image import convert_from_bytes, convert_from_path, pdfinfo_from_path

# Some help functions 
def get_conf(page_gray):
    '''return a average confidence value of OCR result '''
    df = pytesseract.image_to_data(page_gray,output_type='data.frame')
    df.drop(df[df.conf==-1].index.values,inplace=True)
    df.reset_index()
    return df.conf.mean()
  
def deskew(image):
    '''deskew the image'''
    gray = cv2.bitwise_not(image)
    temp_arr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(temp_arr > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated
  
'''
Main part of OCR:
pages_df: save eextracted text for each pdf file, index by page
OCR_dic : dict for saving df of each pdf, filename is the key
'''


work_dir = './'
file_list = ['aa.pdf']

# %%time 
OCR_dic={} 
for file in file_list:
    # convert pdf into image
    fn = os.path.join(work_dir,file)
    print(f"processing {fn}")
    # TODO: somehow this is not working...
    # pdf_file = convert_from_bytes(open(fn, 'rb').read())

    pdf_info = pdfinfo_from_path(fn)
    print(pdf_info)

    # TODO: somehow this is not working...
    pdf_file = convert_from_path(fn, fmt="jpeg")
    # create a df to save each pdf's text
    print(pdf_file)

    pages_df = pd.DataFrame(columns=['conf','text'])
    for (i,page) in enumerate(pdf_file) :
        try:
            print(i)
            print(page)
            # transfer image of pdf_file into array
            page_arr = np.asarray(page)
            # transfer into grayscale
            page_arr_gray = cv2.cvtColor(page_arr,cv2.COLOR_BGR2GRAY)
            # deskew the page
            page_deskew = deskew(page_arr_gray)
            # cal confidence value
            page_conf = get_conf(page_deskew)
            # extract string 
            page_text = pytesseract.image_to_string(page_deskew)
            print('-----page_conf-----')
            print(page_conf)
            print('-----page_text-----')
            print(page_text)
            pages_df = pages_df.append({'conf': page_conf,'text': page_text}, ignore_index=True)
        except:
            print('error.......')
            # if can't extract then give some notes into df
            pages_df = pages_df.append({'conf': -1,'text': 'N/A'}, ignore_index=True)
            continue
    # save df into a dict with filename as key        
    OCR_dic[file]=pages_df
    print('{} is done'.format(file))
