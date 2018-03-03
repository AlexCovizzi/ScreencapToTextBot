import requests
import configparser
import constants as c
import logging
log = logging.getLogger(__name__)

# parse configuration file
parser = configparser.ConfigParser()
parser.read(c.CONFIG_FILE_NAME)
options = parser["azure"]
ocr_url = options["ocr_url"]
subscription_key = options["subscription_key"]

def analyze(imgBuf):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'en', 'detectOrientation ': 'true'}

    log.info("Sending request to Azure OCR service...")
    response = requests.post(ocr_url, headers=headers, params=params, data=imgBuf)
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.exception("Error requesting Azure OCR service: {}".format(str(e)))
        return []

    analysis = response.json()
    lines = extractLines(analysis)

    return lines

# return list of lines dict(text, left, top, w, h)
def extractLines(analysis):
    lines = []
    regions = analysis["regions"]
    for region in regions:
        for line_info in region["lines"]:
            boundingBox = line_info["boundingBox"].split(",")
            line = {"left": int(boundingBox[0]), "top": int(boundingBox[1]), "w": int(boundingBox[2]), "h": int(boundingBox[3])}
            text = ""
            for i, word_info in enumerate(line_info["words"]):
                if i > 0:
                    text += " "
                text += word_info["text"]

            line["text"] = text
            lines.append(line)

    lines = joinLinesInSameY(lines)
    lines = sortLinesByY(lines)

    return lines

def joinLinesInSameY(lines_old):
    lines = []
    while(len(lines_old) > 0):
        line = lines_old.pop(0)
        for l in lines_old[:]:
            if l["top"]-8 < line["top"] < l["top"]+8:
                if line["left"] < l["left"]:
                    line["text"] += " "+l["text"]
                else:
                    line["text"] = l["text"] + " " +line["text"]
                
                lines_old.remove(l)
        lines.append(line)
    return lines

def sortLinesByY(lines_old):
    lines = []
    while(len(lines_old) > 0):
        line = lines_old[0]
        for l in lines_old:
            if l["top"] < line["top"]:
                line = l
        lines.append(line)
        lines_old.remove(line)
    return lines
