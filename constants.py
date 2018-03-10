CONFIG_FILE_NAME = "config.ini"

# Bot
BOT_NAME = "ScreencapToTextBot"
BOT_VERSION = "0.1"
BOT_REDDIT_USERNAME = "ScreencapToTextBot"
SCORE_DELETE_THRESH = -1 # if a comment has score <= of threshold, it's deleted
SCORE_CHECK_TIME = 60 # time to wait every loop to check the comments score

# Logging
LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
LOG_LEVEL = 20 # DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50

# regex
IMAGE_URL_REGEX = r"https?:\/\/i\.(?:redd\.it|imgur\.com)\/\w+\.(?:jpg|jpeg|png)"
IMGUR_SINGLE_REGEX = r"https?:\/\/imgur\.com\/\w+"
TINDER_NAME_REGEX = u"^[A-Z][a-zà-ü]{2,12}$"
TINDER_DATE_REGEX = r"^[A-Z][a-z]{4,10} [0-9][0-9]?:[0-9][0-9] ?(?:AM|PM)?$"
SOFT_KEYBOARD_REGEX = r"^(GIF)?(.)?(?:Type|Send|Your) (a )?[mM]essage?(\.){0,3}( here)?( Send)?$"

# subreddits (separated by +)
SUBREDDITS = "sttbplayground"
TIMEOUT = 60

# image
IMG_WIDTH = 720

BLUE_BOUNDS = ([190, 160, 0], [255, 212, 110])
GRAY_BOUNDS = ([220, 220, 220], [245, 245, 245])

BLUE = "azure"
GRAY = "gray"

# footer
COMMENT_FOOTER ='''
***
^(I am a bot and this comment was added to help redditors with slow internet or data caps | )^[Contact](https://www.reddit.com/message/compose/?to=duast) ^| ^[Code](https://github.com/AlexCovizzi/ScreencapToTextBot) ^(| -1 to remove)
'''
