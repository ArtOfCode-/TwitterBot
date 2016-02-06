import datetime
from queue import Queue
from threading import Thread
import string
import random

from Module import Command
import SaveIO

save_subdir = 'twitter'

tweet_queue = Queue()


def put_tweet(tweet_id, dt, tweet_text):
    tweets = SaveIO.load(save_subdir, 'tweets')
    tweets[tweet_id] = [dt, tweet_text]
    SaveIO.save(tweets, save_subdir, 'tweets')


def file_writer():
    while True:
        tweet_obj = tweet_queue.get()
        put_tweet(*tweet_obj)
        tweet_queue.task_done()


def on_bot_load(bot):
    thread = Thread(target=file_writer)
    thread.start()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def tweet(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."
    try:
        delay = int(args[0])
        if delay < 0:
            return "Can't schedule a tweet in the past."
    except ValueError:
        return "Invalid arguments."
    
    tweet_text = ' '.join(args[1:])
    if len(tweet_text) > 140:
        return "Unable to schedule tweet since its length exceeds 144 characters."
    
    dt = datetime.datetime.now() + datetime.timedelta(seconds=60*delay)
    tweet_id = id_generator()
    tweet_queue.put_nowait((tweet_id, dt, tweet_text))
    return "scheduled tweet: \n%s \ntime: %s \nid: %s" % (tweet_text, str(dt), tweet_id)


commands = [  # A list of all Commands in this Module.
    Command('tweet', tweet, 'Schedules a tweet. Syntax: $PREFIXtweet <delay> (in minutes) <tweet>',
            True, False, None, None)
]

module_name = "twitter"
