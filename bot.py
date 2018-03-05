import time
import re
import constants as c
import sctt
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
        log.info("Processing submission {}".format(submission.id))
        if not isSubmissionValid(submission):
            log.info("Discarded submission {}: invalid (not an image)".format(submission.id))
            return
            
        comment = sctt.process(submission.url)
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

# check if the submission is an image
def isSubmissionValid(submission):
    url_is_image = re.match(c.IMAGE_URL_REGEX, submission.url)
    return url_is_image