import sys
import webbrowser

import requests
import tweepy

import SaveIO
from Config import *

save_subdir = "oauth"

data = None
defaults = {
    'consumer_key': '7TowgTbCOSmjKSqdE41kaGHtT'
}

auth_handler = None


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
    global data
    global auth_handler
    data = SaveIO.load(save_subdir, "keys_data")
    if data == {}:
        defaults['consumer_secret'] = get_secret()
        data = defaults
        SaveIO.save(data, save_subdir, "keys_data")

    auth_handler = tweepy.OAuthHandler(data['consumer_key'], data['consumer_secret'])
    if "access_token" in data and "access_token_secret" in data:
        auth_handler.set_access_token(data['access_token'], data['access_token_secret'])
    else:
        try:
            redirect_url = auth_handler.get_authorization_url()
        except tweepy.TweepError:
            print("[oauth] [tweepy] FATAL: Failed to get authorization URL.")
            sys.exit(503)
        webbrowser.open_new_tab(redirect_url)
        verifier = input("[oauth] Type the verification code from Twitter: ")
        try:
            access_token, access_token_secret = auth_handler.get_access_token(verifier)
        except tweepy.TweepError:
            print("[oauth] [tweepy] FATAL: Could not fetch access token with provided verifier code.")
            sys.exit(504)
        data['access_token'], data['access_token_secret'] = access_token, access_token_secret
        SaveIO.save(data, save_subdir, "keys_data")
        auth_handler.set_access_token(access_token, access_token_secret)


def get_auth_handler():
    global auth_handler
    return auth_handler


def get_authorized_api():
    global auth_handler
    return tweepy.API(auth_handler)


def on_bot_stop(bot):
    global data
    SaveIO.save(data, save_subdir, "keys_data")


commands = []
module_name = "oauth"
