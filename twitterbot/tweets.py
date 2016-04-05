from . import oauth, shortlinks
from Config import Config

def do_tweet(**kwargs):
    api = oauth.get_authorized_api()
    api.update_status(kwargs.get('text'))


def create_tweet_for(item):
    text = Config.Tweets['text']
    text.replace('$Title', item['title'])
    text.replace('$ShortLink', shortlinks.get_shortlink(item['share_link']))
    if len(text) <= 140:
        return text
    else
        raise ValueError("Text is too long to be Tweeted.")
