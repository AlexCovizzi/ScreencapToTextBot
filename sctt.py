# Screencap to text module

import azureocr
import re
import constants as c
import dimage
import exceptions
import ocv
from random import randint
import logging
log = logging.getLogger(__name__)

# convert a screencap (from url) to formatted reddit text
def process(url):
    # download and resize image
    imgBuf = dimage.get(url)
    # find bounding rects of message bubbles with opencv
    rects = ocv.analyze(imgBuf)
    # if the list is empty we can assume that the screencap is not a conversation
    # Note: before azureocr so that no useless request is sent to azure ocr service
    if not rects:
        return ""

    # temporary check to avoid spamming every submission
    # Note: this is temporary!!!
    if randint(1,3) != 1:
        return ""

    # send data to azure
    lines = azureocr.analyze(imgBuf)
    # if the are no lines something went wrong in the request to azure or there is no text
    if not lines:
        return ""

    log.info("Converting to reddit formatted text...")
    conversation = linesToConversation(lines, rects)
    text = formatConversation(conversation)

    return text

# return a list of messages
# message: { author, text }
# author: OP or Other or None (for other type of message)
# text: text of the message
def linesToConversation(lines, rects):
    conversation = []

    lineInRect = False # at least one line is in a rectangle
    lastRectIndex = -1
    otherName = "Other"
    for line in lines:
            
        rectIndex = getLineRectIndex(line, rects)
        if rectIndex is not None:

            if not isTextValid(line["text"]):
                continue

            lineInRect = True
            rect = rects[rectIndex]
            if rectIndex == lastRectIndex:
                conversation[-1]["text"] += " "+line["text"]
            else:
                lastRectIndex = rectIndex
                author = otherName
                if rect["left"]+rect["w"] > c.IMG_WIDTH-c.IMG_WIDTH/10:
                    author = "OP"
                message = { "author": author, "text": line["text"]}
                conversation.append(message)
        else:
            lastRectIndex = -1
            # the line could be the name of the other person
            if isTextName(line["text"]):
                otherName = line["text"]
            else:
                message = { "author":None, "text":line["text"]}
                conversation.append(message)

    # if at least one line is in a rect it means the image is a screencap of
    # a conversation, if not, it's safe to assume the image is not a conversation
    if lineInRect:
        return conversation
    else:
        return []

def getLineRectIndex(line, rects):
    for i, rect in enumerate(rects):
        if isLineInRect(line, rect):
            return i
    return None

def isLineInRect(line, rect):
    cX = rect["left"]-8 < line["left"] < line["left"] + line["w"] < rect["left"] + rect["w"]+8
    cY = rect["top"]-8 < line["top"] < line["top"] + line["h"] < rect["top"] + rect["h"]+8
    return cX and cY

def isTextValid(text):
    match = re.match(c.SOFT_KEYBOARD_REGEX, text)
    return not (match or text == "GIF" or text == "Send")

def isTextName(text):
    match = re.match(c.TINDER_NAME_REGEX, text)
    if match and text != "Sent":
        return True
    else:
        return False

        
def formatConversation(conversation):
    text = ""
    for message in conversation:
        if message["author"]:
            formattedText = formatTextForReddit(message["text"], ["*", "^", "\\", ">", "#"])
            text += "**{}**: {}\n\n".format(message["author"], formattedText)
        #else:
            #text += "^({})\n\n".format(message["text"])
            #match = re.match(c.TINDER_DATE_REGEX, message["text"])
            #if match:
                #text += "^({})\n\n".format(message["text"])

    return text

def formatTextForReddit(text, chars):
    i = 0
    while i < len(text):
        if text[i] in chars:
            text = text[:i]+"\\"+text[i:]
            i+=1
        i+=1
    return text