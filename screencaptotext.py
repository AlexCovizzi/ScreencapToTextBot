from PIL import Image
import cv2
import numpy as np
import pytesseract

def convert(pil_img):
    lines = ocr(pil_img)
    boxes = message_boxes(pil_img)
    
    for box in boxes:
        box["text"] = ""
        for line in lines:
            if is_line_in_box(line, box):
                box["text"] += " "+line["text"]
    
    return boxes

def is_line_in_box(line, box):
    cX = box["x1"] < line["x1"] < line["x2"] < box["x2"]
    cY = box["y1"] < line["y1"] < line["y2"] < box["y2"]
    return cX and cY

def ocr(pil_img):
    prep_img = ocr_preprocess(pil_img)
    lines = ocr_tesseract(prep_img)
    prep_img.close()

    return lines

def ocr_preprocess(pil_img):
    cv_img = np.array(pil_img, dtype=np.uint8)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    #cv_img = contrast(cv_img, alpha=2, beta=-120)
    cv_img = contrast(cv_img)
    return Image.fromarray(cv_img)

def ocr_tesseract(pil_img):
    string = pytesseract.image_to_boxes(pil_img, lang="eng")
    lines = tesseract_string_to_lines(string, pil_img.size[1])
    return lines

def tesseract_string_to_lines(string, img_height):
    rows = string.split("\n")

    chars = []
    for row in rows:
        tokens = row.split(" ")
        char = {'text':tokens[0], 'x1':int(tokens[1]), 'y1':img_height-int(tokens[4]), 'x2':int(tokens[3]), 'y2':img_height-int(tokens[2])}
        chars.append(char)

    words = chars_to_words(chars)
    lines = words_to_lines(words)

    return lines

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

def message_boxes(pil_img):
    boxes = []
    img = np.array(pil_img, dtype=np.uint8)
    cv_img = img.copy()
    # preprocess
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    cv_img = cv2.medianBlur(cv_img, 7)
    cv_img = contrast(cv_img, 7, -210)
    cv_img = cv2.Canny(cv_img, 40, 60, apertureSize=5)
    
    _,contours,_ = cv2.findContours(cv_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv2.drawContours(img, contours, -1, (0,255,0),2)
        if is_contour_message_box(cnt):
            x, y, w, h = cv2.boundingRect(cnt)
            box = {"x1":x, "y1":y, "x2":x+w, "y2":y+h}
            boxes.append(box)
            cv2.rectangle(img, (box["x1"], box["y1"]), (box["x2"], box["y2"]), (0, 0, 255), 3)
    
    boxes.sort(key=lambda y: y["y1"])

    cv2.imshow('img', cv2.resize(img, (0,0), fx=0.5, fy=0.5))
    cv2.waitKey(0)
    
    return boxes

def is_contour_message_box(cnt):
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
    if vertical > 6 and horizontal > 18:
        return True
    else:
        return False

def contrast(cv_img, alpha=1.5, beta=-60.0):
    array_alpha = np.array([float(alpha)])
    array_beta = np.array([float(beta)])

    cv_img = cv2.add(cv_img, array_beta)
    cv_img = cv2.multiply(cv_img, array_alpha)
    
    return cv_img

if __name__ == "__main__":
    import downloadimage

    urls = ["https://i.redd.it/0cpv14gtnin01.png", "https://i.redd.it/i2wn7qgrton01.jpg","https://i.redd.it/ghkm5j563hn01.jpg","https://i.redd.it/6kszvpdyjgn01.png"]
    for url in urls:
        pil_img = downloadimage.get(url)
        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        boxes = message_boxes(pil_img)
            