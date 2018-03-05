from bot import Bot
import time
import praw
from exceptions import CriticalException, MinorException
from prawcore.exceptions import PrawcoreException, InvalidToken
from praw.exceptions import PRAWException, ClientException, APIException
import constants as c
import threading
import configparser
import time
import logging
# setup logging
logging.basicConfig(level=c.LOG_LEVEL,format=c.LOG_FORMAT)
log = logging.getLogger(__name__)


parser = configparser.ConfigParser()
parser.read(c.CONFIG_FILE_NAME)
options = parser['bot']
client_id = options["client_id"]
client_secret = options["client_secret"]
username = options["username"]
password = options["password"]
user_agent = options["user_agent"]

def main():
    reddit = praw.Reddit(
        client_id=client_id, 
        client_secret=client_secret, 
        username=username, password=password, 
        user_agent=user_agent
    )

    clThread = threading.Thread(target=runCleaning, args=(reddit,))
    clThread.setDaemon(True)
    clThread.start()

    bot = Bot(reddit)
    
    while not bot.stopped:
        try:
            bot.run()
        except KeyboardInterrupt:
            log.info('Termination received. Stopping bot...')
            bot.stop()
        except MinorException as e:
            log.exception(str(e))
            log.info("Waiting {} seconds".format(str(c.TIMEOUT)))
            time.sleep(c.TIMEOUT)
        except CriticalException as e:
            log.error(str(e))
            bot.stop()
            running = False

def runCleaning(reddit):
    running = True
    while running:
        try:
            #log.info("Checking bot's comments")
            redditor = reddit.redditor(c.BOT_REDDIT_USERNAME)
            for comment in redditor.comments.new(limit=50):
                if comment.score <= c.SCORE_DELETE_THRESH:
                    comment.delete()
                    log.info("Comment to {} deleted (score: {})".format(comment.parent_id, comment.score))

            time.sleep(c.SCORE_CHECK_TIME)
        except (PrawcoreException, APIException, ClientException) as e:
            log.exception("Error parsing bot's comments: {}".format(str(e)))
            log.info("Waiting {} seconds".format(str(c.TIMEOUT)))
            time.sleep(c.TIMEOUT)

if __name__ == "__main__":
    main()