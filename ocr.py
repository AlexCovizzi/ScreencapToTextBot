from PIL import Image
import cv2
import numpy as np
import pytesseract
from statistics import mode
import time

TESSERACT_CONFIG = "-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.=!%&/\?*()^-_ -psm 6"

# img PIL Image
# bounds (X1, Y1, X2, Y2)
def analyze(pil_img, bounds = None):
    if bounds: pil_img = pil_img.crop(bounds)
    pil_img = preprocess(pil_img)
    if pil_img:
        #pil_img.show()
        text = pytesseract.image_to_string(pil_img, lang="eng")
        return text
    return ""

def preprocess(pil_img):
    start_time = time.time()

    cv_img = np.array(pil_img)

    hls = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HLS)
    try: light = get_mode_lightness(hls)
    except: return None
    
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    if light < 160:
        ret, cv_img = cv2.threshold(cv_img,212,255,cv2.THRESH_BINARY)
    else:
        ret, cv_img = cv2.threshold(cv_img,96,255,cv2.THRESH_BINARY_INV)

    cv_img = remove_white_corners(cv_img)

    #cv_img = cv2.add(white, black)

    #cv_img = cv2.Canny(cv_img, 0, 100, apertureSize=3)
    #cv_img = cv2.medianBlur(cv_img, 3)
    #cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
    #cv_img = cv2.erode(cv_img, None)
    #cv_img = cv2.dilate(cv_img, None)
    #cv_img = cv2.fastNlMeansDenoising(cv_img, None, 40)

    end_time = time.time()

    #print(end_time - start_time)

    return Image.fromarray(cv_img)

# remove white corners from the image so that
# tesseract does not interpret it as text
def remove_white_corners(cv_img):
    for px_row in cv_img:
        k = 0
        for i, px in enumerate(px_row):
            if px > 0:
                px_row[i] = 0
                k = 0
            else:
                k += 1
                if k > 8:
                    break
        k = 0
        for i, px in reversed(list(enumerate(px_row))):
            if px > 0:
                px_row[i] = 0
                k = 0
            else:
                k += 1
                if k > 8:
                    break

    for px_row in cv_img.T:
        k = 0
        for i, px in enumerate(px_row):
            if px > 0:
                px_row[i] = 0
                k = 0
            else:
                k += 1
                if k > 8:
                    break
        k = 0
        for i, px in reversed(list(enumerate(px_row))):
            if px > 0:
                px_row[i] = 0
                k = 0
            else:
                k += 1
                if k > 8:
                    break

    return cv_img

def get_mode_lightness(hls_img):
    px_row = [px[1] for px in hls_img[int(len(hls_img)/2+1)]]
    return mode(px_row)

if __name__ == '__main__':
    pass