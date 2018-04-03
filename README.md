# ScreencapToTextBot
Reddit bot that takes the screencap of a conversation and converts it in reddit formatted text.
## How it works
The bot uses a combination of OCR (Optical Character Recognition) and image manipulation.

The OCR part is done with [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/), so the bot, after downloading the image, sends the data to the Azure API that responds with a JSON containing informations about the text in the image and its position.

The image manipulation is done with [OpenCV](https://opencv.org/). Using OpenCV the bot can find the message boxes based on their color (gray, blue).

Finally those two results are put together: if the text is inside the box, it means it's a message otherwise it means it's useless data (date, time, cell info etc). The message is then assigned to **OP** if it's on the right or to **Other** if it's on the left.

**Note**: This bot is tailored for the subreddit r/Tinder, it can only recognize message boxes gray or blue (a conversation in Tinder), if none is found, the submission is discarded.

**Note 2**: The bot is banned from r/Tinder