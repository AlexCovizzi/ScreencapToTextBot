import praw
import configparser
import time
import logging
log = logging.getLogger(__name__)

parser = configparser.ConfigParser()
parser.read("config.ini")
options = parser['bot']
client_id = options["client_id"]
client_secret = options["client_secret"]
username = options["username"]
password = options["password"]
user_agent = options["user_agent"]

SRC_SUB = "tinder"
DST_SUB = "sttbplayground"

LIMIT = 10

def main():
    reddit = praw.Reddit(
        client_id=client_id, 
        client_secret=client_secret, 
        username=username, password=password, 
        user_agent=user_agent
    )
    src_subreddit = reddit.subreddit(SRC_SUB)
    dst_subreddit = reddit.subreddit(DST_SUB)

    try:
        postNew(src_subreddit, dst_subreddit, LIMIT)
    except KeyboardInterrupt:
        log.info("Interrupted")
        pass
    
    log.info("Closed bot.")

def postStream(src_subreddit, dst_subreddit, limit):
    started_at = time.time()
    i = 0
    for submission in src_subreddit.stream.submissions():
        if i >= limit:
            break
        # old submissions are discarded
        if submission.created_utc > started_at:
            log.info("Submitted {}".format(submission.id))
            dst_subreddit.submit(submission.title, url=submission.url)
            i += 1


def postNew(src_subreddit, dst_subreddit, limit):
    submissions = src_subreddit.hot(limit=limit)
    for submission in submissions:
        log.info("Submitted {}".format(submission.id))
        dst_subreddit.submit(submission.title, url=submission.url)
            

if __name__ == "__main__":
    main()
