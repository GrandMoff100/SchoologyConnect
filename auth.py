import os
import sys
import pickle
from schoolopy import Auth, Schoology
from urllib.parse import urlparse, parse_qs, urlencode


APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
sys.setrecursionlimit(1_000_000)


class District833User:
    DOMAIN = 'https://learn.sowashco.org'

    sc = None

    def __init__(self):
        self.auth = Auth(
            APP_KEY,
            APP_SECRET,
            domain=self.DOMAIN,
            three_legged=True
        )

    def request_url(self, callback_url):
        url = self.auth.request_authorization()
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)
        self.oauth_token = query_dict.get('oauth_token')[0]
        query_dict.update(
            oauth_callback=callback_url,
            oauth_token=self.oauth_token
        )
        return url.replace(parsed.query, urlencode(query_dict))

    def validate_auth(self):
        if self.auth.authorize():
            self.sc = Schoology(self.auth)
            return True
        return False

    def config_sc(self):
        if self.sc:
            self.sc.limit = 10

    def tobin(self):
        return pickle.dumps(self)
