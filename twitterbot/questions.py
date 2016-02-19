import threading
import sys
from time import sleep
from datetime import datetime

import apipy

from Config import Config

module_name = "questions"
save_subdir = "twb_questions"
commands = []

thread_handle = None
thread_terminate = False


def on_bot_load(bot):
    global thread_handle
    thread_handle = threading.Thread(target=questions_thread, kwargs={'bot': bot})
    thread_handle.start()


def on_bot_stop(bot):
    global thread_handle, thread_terminate
    print("Terminating background API thread...")
    thread_terminate = True
    thread_handle.join(Config.Questions['cycle_timeout'] + 1)
    if thread_handle.is_alive():
        print("Thread could not be terminated - program will exit, but thread may continue.")
        sys.exit(601)


def questions_thread(**kwargs):
    bot = kwargs.get('bot')
    requester = apipy.APIRequester(Config.Questions['api_key'], Config.Questions['api_id'])
    multiplier = 1
    last_checked = None
    while not thread_terminate:
        response = requester.make_request("/questions", {
            'pagesize': 100,
            'site': 'worldbuilding',
            'filter': '!-NA3hm*ngiTSYRTK(sa-P-n.5IICut5tL'
        })
        if not response.is_error():
            items = response.get_items()
            for item in items:
                if item['question_id'] == last_checked:
                    multiplier *= 2
                    break
                else:
                    if days_old(item['creation_date']) > Config.Questions['days_old'] and \
                       item['score'] >= Config.Questions['score'] and \
                       item['answer_count'] >= Config.Questions['answer_count'] and \
                       item['close_vote_count'] <= Config.Questions['close_votes'] and \
                       ('closed_reason' not in item or item['closed_reason'] is None) and \
                       item['delete_vote_count'] <= Config.Questions['delete_votes'] and \
                       controversy(item['up_vote_count'], item['down_vote_count']) <= Config.Questions['controversy'] and \
                       ('locked_date' not in item or item['locked_date'] is None) and \
                       ('notice' not in item or item['notice'] is None):
                        bot.room.send_message("Tweetable: {0}".format(item['share_link']))
            last_checked = items[0]['question_id']
        else:
            multiplier *= 3
            print("Response from the API was an error: {0}".format(response.get_wrapper()['error_message']))

        sleep(Config.Questions['cycle_timeout'] * multiplier)
        multiplier = 1


def days_old(dt):
    dt_obj = datetime.fromtimestamp(dt / 1e3)
    delta = datetime.now() - dt_obj
    return delta.days


def controversy(up, down):
    return float(down) / float(up)
