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
    url = "https://i.imgur.com/7nwQs7o.jpg"
    pil_img = downloadimage.get(url)

    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.uint8), cv2.COLOR_RGB2BGR)

    pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY))
    string_boxes = pytesseract.image_to_boxes(pil_img, lang="eng")
    rows = string_boxes.split("\n")
    chars = []
    hsize = cv_img.shape[0]
    for row in rows:
        tokens = row.split(" ")
        char = {'text':tokens[0], 'x1':int(tokens[1]), 'y1':hsize-int(tokens[2]), 'x2':int(tokens[3]), 'y2':hsize-int(tokens[4])}
        chars.append(char)

    words = [chars[0]]
    for char in chars[1:]:
        last = words[-1]
        if last['x2']-4 < char['x1'] < last['x2']+12 and ( last['y1']-12 < char['y1'] < last['y1']+12 or last['y2']-12 < char['y2'] < last['y2']+12 ):
            last['text'] += char['text']
            last['x2'] = char['x2']
            if char['y1'] < last['y1']: last['y1'] = char['y1']
            if char['y2'] > last['y2']: last['y2'] = char['y2']
        else:
            words.append(char)

    lines = [words[0]]
    for word in words[1:]:
        last = lines[-1]
        if last['x2']-4 < word['x1'] < last['x2']+40 and ( last['y1']-12 < word['y1'] < last['y1']+12 or last['y2']-12 < word['y2'] < last['y2']+12 ):
            last['text'] += " "+word['text']
            last['x2'] = word['x2']
        else:
            lines.append(word)

    for line in lines:
        print(line)

    '''
    per prima cosa prendo il canale saturazione,
    ed estraggo le forme semi-rettangolari
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