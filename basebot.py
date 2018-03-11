# base class for every other bot
import praw
from concurrent.futures import ThreadPoolExecutor
import logging
log = logging.getLogger(__name__)

class BaseBot:

    def __init__(self, client_id, client_secret, user_agent, username, password, multi_thread=False, max_workers=2, timeout=10, max_retry=2):
        self.reddit = praw.Reddit (
            client_id=client_id,
            client_secret=client_secret,
            username=username, password=password,
            user_agent=user_agent
        )

        self.multi_thread = multi_thread
        if multi_thread:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            self.retry_timeout = retry_timeout

    def run(self, repeat=False, time=60, timeout=10):
        self.repeat = repeat
        while(repeat):
            contents = self.fetch(self.reddit)
            for content in contents:
                if multi_thread:
                    p = executor.submit(process, content)

    # fetch something from reddit, must return a list
    def fetch(self, reddit):
        pass

    # content can be submission, comment, etc
    # to be implemented
    def process(content):
        pass

    def stop():
        self.repeat = False
        log.info("Bot stopped.")

