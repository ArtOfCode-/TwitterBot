import importlib.util
spec = importlib.util.spec_from_file_location("auth", "twitterbot/tweepy/tweepy")
tweepy_auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tweepy_auth)

def on_bot_load(bot):
    auth_handler = tweepy_auth.OAuthHandler("a", "a")

commands = []
