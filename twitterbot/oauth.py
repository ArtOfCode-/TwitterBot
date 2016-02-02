import json
import requests
import SaveIO
import sys
from Config import *
import importlib.util
spec = importlib.util.spec_from_file_location("auth", "twitterbot/tweepy/tweepy")
tweepy_lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tweepy_lib)


save_subdir = "oauth"

data = None
defaults = {
    'consumer_key': '7TowgTbCOSmjKSqdE41kaGHtT'
}


def get_secret():
    if "secret_url" and "secret_key" in Config.General:
        json_return = json.loads(requests.get("{0}?request_key={1}".format(Config.General['secret_url'],
                                                                           Config.General['secret_key'])))
        if "key" in json_return:
            return json['key']
        else:
            print("[oauth] FATAL: No secret provided in fetch response.")
            print("[oauth] full error: {0} - {1}".format(json['error_name'], json['error_message']))
            sys.exit(501)

    else:
        print("[oauth] FATAL: No URL or key was provided to fetch consumer secret.")
        sys.exit(502)


def on_bot_load(bot):
    global data
    data = SaveIO.load(save_subdir, "keys_data")
    if data == {}:
        defaults['consumer_secret'] = get_secret()
        data = defaults
        SaveIO.save(data, save_subdir, "keys_data")


def on_bot_stop(bot):
    global data
    SaveIO.save(data, save_subdir, "keys_data")


commands = []
