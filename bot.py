import time
import re
import constants as c
import sctt
import imgur
from prawcore.exceptions import PrawcoreException, InvalidToken
from praw.exceptions import PRAWException, ClientException, APIException
from exceptions import MinorException, CriticalException
import logging
log = logging.getLogger(__name__)

class Bot:
    
    def __init__(self, reddit):
        log.info("Bot {} initializing".format(c.BOT_NAME))
        self.reddit = reddit
        self.stopped = False

    def run(self):
        log.info("Bot {} started.".format(c.BOT_NAME))

        try:
            started_at = time.time()
            subreddit = self.reddit.subreddit(c.SUBREDDITS)

            for submission in subreddit.stream.submissions():
                # old submissions are discarded
                if submission.created_utc < started_at:
                    continue

                self.processSubmission(submission)

        except (ClientException, InvalidToken) as e:
            # something wrong with the client, this should not happen
            # for critical exceptions the bot will stop
            # handled by main.py
            raise CriticalException("Error processing subreddit stream: {}".format(str(e)))
        except (PrawcoreException, APIException) as e:
            # for minor exceptions the bot will wait a timeout and retry running again
            # handled by main.py
            raise MinorException("Error processing subreddit stream: {}".format(str(e)))

    def stop(self):
        self.stopped = True
        log.info("Bot {} stopped.".format(c.BOT_NAME))

    def processSubmission(self, submission):
        log.info("Processing submission {}: {}".format(submission.id, submission.url))
        url = getUrlFromSubmission(submission)
        if not url:
            log.info("Discarded submission {}: invalid (not an image)".format(submission.id))
            return
            
        comment = sctt.process(url)
        # reply only if the comment is not an empty string
        # if the string is empty it means something went wrong or the
        # screencap is not a conversation
        if comment:
            reply(submission, comment)
        else:
            log.info("Discarded submission {}".format(submission.id))

# class bot end

# reddit utils
def reply(submission, comment):
    comment += c.COMMENT_FOOTER
    submission.reply(comment)
    log.info("Replied to submission {}".format(submission.id))

# get image url from the submission or None if the submission is invalid
def getUrlFromSubmission(submission):
    url = submission.url
    url_is_image = re.match(c.IMAGE_URL_REGEX, url)
    # the url is already an image on "i.redd.it" or "i.imgur.com"
    if url_is_image:
        return url
    match = re.match(c.IMGUR_SINGLE_REGEX, url)
    # the url is a link to a single image post on imgur
    if match:
        return imgur.imageUrlFromSingle(url)
    
    # the image is invalid (text, album, etc)
    return None