# supervised test

import ocv
import dimage
import praw
import re
import constants as c
import configparser

parser = configparser.ConfigParser()
parser.read(c.CONFIG_FILE_NAME)
options = parser['bot']
client_id = options["client_id"]
client_secret = options["client_secret"]
username = options["username"]
password = options["password"]
user_agent = options["user_agent"]

SUBREDDITS = ["Tinder"]

def main():
    urls = findValidSubmissionsUrl(SUBREDDITS)
    for url in urls:
        print("Image url: "+url)
        # download image
        imgBuf = dimage.get(url)
        try:
            ocv.analyze(imgBuf, debug = True)
        except:
            pass

def findValidSubmissionsUrl(subreddits):
    urls = []
    reddit = praw.Reddit(
                client_id=client_id, 
                client_secret=client_secret, 
                username=username, password=password, 
                user_agent=user_agent
            )
    for subredditName in subreddits:
        subreddit = reddit.subreddit(subredditName)
        submissions = getSubmissions(subreddit, 20)
        for submission in submissions:
            urls.append(submission.url)
    
    return urls

def getSubmissions(subreddit, submissions_limit):
    submissions = []
    for submission in subreddit.new(limit=submissions_limit):
        if isSubmissionValid(submission):
            submissions.append(submission)

    return submissions

def isSubmissionValid(submission):
    urlImage = isUrlImage(submission.url)
    return urlImage

def isUrlImage(url):
    match = re.match(c.IMAGE_URL_REGEX, url)
    return (match is not None)

if __name__ == "__main__":
    main()
