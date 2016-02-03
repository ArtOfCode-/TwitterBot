import json
import requests
import SaveIO
import sys
from Config import *
# import tweepy


save_subdir = "oauth"

data = None
defaults = {
    'consumer_key': '7TowgTbCOSmjKSqdE41kaGHtT'
}


def get_secret():
    if "secret_url" and "secret_key" in Config.General:
        json_return = requests.get("{0}?request_key={1}".format(Config.General['secret_url'],
                                                                Config.General['secret_key'])).json()
        if "secret" in json_return:
            return json_return['secret']
        else:
            print("[oauth] FATAL: No secret provided in fetch response.")
            print("[oauth] full error: {0} - {1}".format(json_return['error_name'], json_return['error_message']))
            sys.exit(501)

    else:
        print("[oauth] FATAL: No URL or key was provided to fetch consumer secret.")
        sys.exit(502)


def on_bot_load(bot):
    print("load")
    global data
    data = SaveIO.load(save_subdir, "keys_data")
    if data == {}:
        print("load new data")
        defaults['consumer_secret'] = get_secret()
        data = defaults
        SaveIO.save(data, save_subdir, "keys_data")
    for k, v in data.items():
        print("{0}: {1}".format(k, v))


def on_bot_stop(bot):
    global data
    SaveIO.save(data, save_subdir, "keys_data")


commands = []
module_name = "oauth"
