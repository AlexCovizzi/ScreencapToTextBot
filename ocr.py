from PIL import Image
import cv2
import numpy as np
import pytesseract

# img PIL Image
# bounds (X1, Y1, X2, Y2)
def analyze(img, bounds = None):
    if bounds: img = img.crop(bounds)
    img = preprocess(img)
    img.show()
    text = pytesseract.image_to_string(img)
    return text

def preprocess(img):
    cv_img = np.array(img)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    ret,gray = cv2.threshold(cv_img,250,255,0)
    mask = np.zeros(cv_img.shape, np.uint8)

    cv_img = cv2.bitwise_and(cv_img, cv_img, mask = mask)

    return Image.fromarray(cv_img)

if __name__ == '__main__':
    img = Image.open('test.jpeg')
    text = analyze(img, (100,170,720,250))
    print(text)