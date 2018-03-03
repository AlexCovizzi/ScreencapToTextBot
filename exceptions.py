
# stops the current iteration in a loop
class MinorException(Exception):
    pass

# stops the bot
class CriticalException(Exception):
    pass