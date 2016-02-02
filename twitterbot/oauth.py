from .tweepy import tweepy

def on_bot_load(bot):
    auth_handler = tweepy.OAuthHandler("a", "a")

commands = []
