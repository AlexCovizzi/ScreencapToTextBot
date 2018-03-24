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
        
    prep_img = preprocess(pil_img)
    lines = tesseract_ocr(prep_img)
    prep_img.close()

    return lines

def preprocess(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    cv_img = contrast(cv_img)
    return Image.fromarray(cv_img)

def tesseract_ocr(pil_img):
    string_boxes = pytesseract.image_to_boxes(pil_img, lang="eng")
    rows = string_boxes.split("\n")

    hsize = pil_img.size[1]
    chars = []
    for row in rows:
        tokens = row.split(" ")
        char = {'text':tokens[0], 'x1':int(tokens[1]), 'y1':hsize-int(tokens[4]), 'x2':int(tokens[3]), 'y2':hsize-int(tokens[2])}
        chars.append(char)

    words = chars_to_words(chars)
    lines = words_to_lines(words)

    return lines

def contrast(cv_img, alpha=1.5, beta=-60.0):
    array_alpha = np.array([float(alpha)])
    array_beta = np.array([float(beta)])

    cv_img = cv2.add(cv_img, array_beta)
    cv_img = cv2.multiply(cv_img, array_alpha)
    
    return cv_img

def chars_to_words(chars):
    words = [chars[0]]
    for char in chars[1:]:
        last = words[-1]
        if last['x2']-2 < char['x1'] < last['x2']+6 and ( last['y1']-8 < char['y1'] < last['y1']+8 or last['y2']-8 < char['y2'] < last['y2']+8 ):
            last['text'] += char['text']
            last['x2'] = char['x2']
            if char['y1'] < last['y1']: last['y1'] = char['y1']
            if char['y2'] > last['y2']: last['y2'] = char['y2']
        else:
            words.append(char)

    return words

def words_to_lines(words):
    lines = [words[0]]
    for word in words[1:]:
        last = lines[-1]
        if last['x2']-2 < word['x1'] < last['x2']+16 and ( last['y1']-6 < word['y1'] < last['y1']+6 or last['y2']-6 < word['y2'] < last['y2']+6 ):
            last['text'] += " "+word['text']
            last['x2'] = word['x2']
        else:
            lines.append(word)

    return lines

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

# devono esserci almeno 1 linea orizzontale e una verticale lunga un tot
def is_contour_message_box(cnt):
    cnt_area = cv2.contourArea(cnt)
    if cnt_area < 1600:
        return False
    cnt_len = cv2.arcLength(cnt, False)
    #cnt = cv2.approxPolyDP(cnt, 0.001*cnt_len, False)
    vertical = 0
    horizontal = 0
    last = cnt[0]
    for point in cnt[1:]:
        x = point[0][0]
        y = point[0][1]
        last_x = last[0][0]
        last_y = last[0][1]
        if x == last_x:
            v = abs(last_y-y)
            if v > vertical: vertical = v
        if y == last_y:
            h = abs(last_x-x)
            if h > horizontal: horizontal = h
        last = point
    #print("Vertical: {}, Horizontal: {}".format(vertical, horizontal))
    if vertical > 12 and horizontal > 16:
        return True
    else:
        return False

if __name__ == '__main__':
    url = "https://i.redd.it/lx032y3l60n01.jpg"
    pil_img = downloadimage.get(url)

    #lines = analyze(pil_img)

    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    gray = contrast(gray, 7.5, -220)
    #cv2.imshow('img', cv2.resize(gray, (0,0), fx=0.4, fy=0.4))
    #cv2.waitKey(0)
    #squares = find_squares(cv_img)
    #cv2.drawContours( cv_img, squares, -1, (0, 255, 0), 3 )

    gray = cv2.Canny(gray, 40, 60, apertureSize=5)
    #cv2.imshow('img', cv2.resize(gray, (0,0), fx=0.4, fy=0.4))
    #cv2.waitKey(0)

    _,contours,_ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(cv_img,contours,-1,(0,0,255),1)

    for cnt in contours:
        if is_contour_message_box(cnt):
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.drawContours(cv_img,[cnt],0,(0,255,0),3)
            

    cv2.imshow('img', cv2.resize(cv_img, (0,0), fx=0.5, fy=0.5))
    cv2.waitKey(0)