from Config import Config
import html.parser as parse
import requests

def get_shortlink(long_url):
    escaped_url = parse.HTMLParser().escape(long_url)
    payload = {
        'longUrl': escaped_url,
        'access_token': Config.ShortLinks['generic_token']
    }
    r = requests.get("{0}{1}".format(Config.ShortLinks['url_base'], Config.ShortLinks['shorten_route']), params=payload)
    r = r.json()
    return r['data']['url']
