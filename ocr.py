from PIL import Image
import cv2
import numpy as np
import pytesseract
from statistics import mode
import time
import downloadimage

TESSERACT_CONFIG = "-c language_model_penalty_non_dict_word=0.5 language_model_penalty_font=0.3 language_model_penalty_case=0.5 tessedit_preserve_min_wd_len=0 language_model_penalty_non_freq_dict_word=0.4 language_model_penalty_chartype=1.2"

# img PIL Image
# bounds (X1, Y1, X2, Y2)
def analyze(pil_img, bounds = None):
    if bounds: pil_img = pil_img.crop(bounds)
        
    pil_img = preprocess(pil_img)
    pil_img.show()
    text = pytesseract.image_to_string(pil_img, lang="eng")#, config=TESSERACT_CONFIG)
    return text

def preprocess(pil_img):
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.uint8), cv2.COLOR_RGB2GRAY)
    #cv_img = cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5)
    
    _,cv_img = cv2.threshold(cv_img,204,255,cv2.THRESH_BINARY)

    # adding a thick white border so that the corners are not read as letters
    border = 10
    cv_img = cv2.copyMakeBorder(cv_img, border, border, border, border, cv2.BORDER_CONSTANT, value=255)

    if cv_img[2][int(cv_img.shape[1]/2)] < 255:
        h, w = cv_img.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(cv_img, mask, (0,0), 0)

    return Image.fromarray(cv_img)

def get_mode_lightness(hls_img):
    px_row = [px[1] for px in hls_img[int(len(hls_img)/2+1)]]
    return mode(px_row)

if __name__ == '__main__':
    url = "https://i.redd.it/5dvar4yyk2n01.png"
    pil_img = downloadimage.get(url)
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.uint8), cv2.COLOR_RGB2HLS)
    h,l,s = cv2.split(cv_img)

    '''
    per prima cosa prendo il canale saturazione,
    ed estraggo le forme semi-rettangolari con
    roba scritta dentro (la roba scritta dentro è in genere bianca)
    poi prendo il canale lightness ed estraggo le forme con dentro
    delle scritte nere
    '''
    
    #_,cv_img = cv2.threshold(cv_img,250,120,cv2.THRESH_BINARY_INV)
    #kernel = np.ones((11,11),np.uint8)
    #cv_img = cv2.erode(cv_img, kernel)
    #cv_img = cv2.medianBlur(cv_img, 5)

    #_,cv_img = cv2.threshold(s,127,255,cv2.THRESH_BINARY)
    #cv_img = cv2.medianBlur(cv_img, 5)

    #_,cv_img = cv2.threshold(v,127,255,cv2.THRESH_BINARY_INV)
    #cv_img = cv2.medianBlur(cv_img, 7)
    #kernel = np.ones((5,5),np.uint8)
    #cv_img = cv2.erode(cv_img, kernel)
    #cv_img = cv2.medianBlur(cv_img, 5)

    cv2.imshow('dst_rt', cv2.resize(l, (0,0), fx=0.3, fy=0.3))
    cv2.waitKey(0)
    cv2.imshow('dst_rt', cv2.resize(s, (0,0), fx=0.3, fy=0.3))
    cv2.waitKey(0)