from bot import Bot
import time
from exceptions import CriticalException, MinorException
import constants as c
import logging
# setup logging
logging.basicConfig(level=c.LOG_LEVEL,format=c.LOG_FORMAT)
log = logging.getLogger(__name__)

def main():
    bot = Bot()
    running = True
    while running:
        try:
            bot.run()
        except KeyboardInterrupt:
            log.info('Termination received. Stopping bot...')
            bot.stop()
            running = False
        except MinorException as e:
            log.exception(str(e))
            log.info("Waiting {} seconds".format(str(c.TIMEOUT)))
            time.sleep(c.TIMEOUT)
        except CriticalException as e:
            log.error(str(e))
            bot.stop()
            running = False

if __name__ == "__main__":
    main()