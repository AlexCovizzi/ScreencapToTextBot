from PIL import Image
import cv2
import numpy as np
import pytesseract
import time

TESSERACT_CONFIG = "-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.=!%&/\?*()^-_ -psm 6"

# img PIL Image
# bounds (X1, Y1, X2, Y2)
def analyze(img, bounds = None):
    if bounds: img = img.crop(bounds)
    img = preprocess(img)
    img.show()
    text = pytesseract.image_to_string(img)
    return text

def preprocess(img):
    start_time = time.time()

    cv_img = np.array(img)

    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    ret,white = cv2.threshold(cv_img,246,255,cv2.THRESH_BINARY)
    
    ret,black = cv2.threshold(cv_img,60,255,cv2.THRESH_BINARY_INV)

    cv_img = cv2.add(white, black)

    #cv_img = cv2.Canny(cv_img, 0, 100, apertureSize=3)
    #cv_img = cv2.medianBlur(cv_img, 3)
    #cv_img = cv2.GaussianBlur(cv_img, (3, 3), 0)
    #cv_img = cv2.erode(cv_img, None)
    #cv_img = cv2.dilate(cv_img, None)
    #cv_img = cv2.fastNlMeansDenoising(cv_img, None, 40) 

    end_time = time.time()

    #print(end_time - start_time)

    return Image.fromarray(cv_img)

def resize(img, new_width):
    wpercent = (new_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    return img.resize((new_width,hsize), Image.ANTIALIAS)

if __name__ == '__main__':
    img = Image.open('test.jpg')
    img = resize(img, 1080)
    #text = analyze(img)
    #text = analyze(img, (0,200,1080,1200))
    #text = analyze(img, (170,540,700,640))
    #text = analyze(img, (340,1080,1400,1280))
    #print(text)