import threading
import sys
from time import sleep
from datetime import datetime
from time import time

import apipy

from Config import Config
import SaveIO
from . import logs

module_name = "questions"
save_subdir = "twb_questions"
commands = []

thread_handle = None
thread_terminate = False

save_data = {
    "request_id": 1,
    "tweeted_ids": {
        # 'question id': 'time checked'
    }
}


def on_bot_load(bot):
    global thread_handle, save_data
    load_data = SaveIO.load(save_subdir, "save_data")
    if load_data is not None:
        save_data = load_data
    thread_handle = threading.Thread(target=questions_thread, kwargs={'bot': bot})
    thread_handle.start()


def on_bot_stop(bot):
    global thread_handle, thread_terminate
    print("Terminating background API thread. You may find it easier to simply end the process.")
    thread_terminate = True
    thread_handle.join(Config.Questions['cycle_timeout'] + 1)
    if thread_handle.is_alive():
        print("Thread could not be terminated - program will exit, but thread may continue.")
        sys.exit(601)


def questions_thread(**kwargs):
    global save_data

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
        request_id = save_data['request_id']
        ids_checked = 0
        ids_tweetable = 0

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
                      ('notice' not in item or item['notice'] is None) and \
                      (str(item['question_id']) not in save_data['tweeted_ids'] or
                      days_old(save_data['tweeted_ids'][str(item['question_id'])]) > Config.Questions['last_tweet']):
                        bot.room.send_message("Tweetable: {0}".format(item['share_link']))
                        ids_tweetable += 1
                        save_data['tweeted_ids'][str(item['question_id'])] = time()
                        SaveIO.save(save_data, save_subdir, "save_data")
                ids_checked += 1

            last_checked = items[0]['question_id']
        else:
            multiplier *= 3
            log = "Response from the API was an error: {0}".format(response.get_wrapper()['error_message'])
            print(log)
            logs.write_log_line(log)

        log = "API request #{0} completed with {1} checked and {2} tweetable.".format(request_id, ids_checked,
                                                                                      ids_tweetable)
        print(log)
        logs.write_log_line(log)

        sleep(Config.Questions['cycle_timeout'] * multiplier)

        multiplier = 1
        save_data['request_id'] += 1
        SaveIO.save(save_data, save_subdir, "save_data")


def days_old(dt):
    dt_obj = datetime.fromtimestamp(dt)
    delta = datetime.now() - dt_obj
    return delta.days


def date_days_old(dt):
    delta = datetime.now() - dt
    return delta.days


def controversy(up, down):
    return float(down) / float(up)
