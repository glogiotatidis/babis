# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

import six
from six.moves.urllib.request import Request, urlopen
from six.moves.urllib.error import URLError


PERIOD_MAP = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 60 * 60 * 24
}


class decorator(object):
    def __init__(self, ping_before=None, ping_after=None, fail_silenty=False,
                 method='GET', user_agent='curl/7.50.1', rate=None):
        self.ping_before = ping_before
        self.ping_after = ping_after
        self.fail_silenty = fail_silenty
        self.method = method
        self.user_agent = user_agent
        if rate:
            self.calls = []
            match = re.match(r'([\d]+)(?:/(\d)?([smhd]))?$', rate)
            if match:
                self.ratelimit_count, multi, ratelimit_period = match.groups()
            else:
                raise Exception('Invalid rate limit')

            try:
                self.ratelimit_count = int(self.ratelimit_count)
            except ValueError:
                raise Exception('Invalid rate limit')

            if not ratelimit_period:
                ratelimit_period = 'm'  # 1 minute
            ratelimit_period = PERIOD_MAP[ratelimit_period]

            if multi:
                ratelimit_period = ratelimit_period * int(multi)

            self.ratelimit_period = ratelimit_period

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            if self.ping_before and not self.is_ratelimited():
                self.ping_urls(self.ping_before)
            fn(*args, **kwargs)
            if self.ping_after and not self.is_ratelimited():
                self.ping_urls(self.ping_after)
        if hasattr(fn, '__name__'):
            wrapped.__name__ = fn.__name__
        return wrapped

    def is_ratelimited(self):
        if not hasattr(self, 'ratelimit_count'):
            return False

        moment = datetime.utcnow()

        # Clear old calls
        delta = timedelta(seconds=self.ratelimit_period)

        self.calls = [call for call in self.calls if (moment - call) < delta]

        if len(self.calls) == self.ratelimit_count:
            return True

        self.calls.append(moment)
        return False

    def ping_urls(self, urls):
        if isinstance(urls, six.string_types):
            self.ping_url(urls)
        else:
            for url in urls:
                self.ping_url(url)

    def ping_url(self, url):
        method = self.method.lower()
        data = None if method == 'get' else ''
        headers = {
            'User-Agent': self.user_agent,
        }
        request = Request(url, data=data, headers=headers)
        try:
            urlopen(request)
        except URLError:
            if not self.fail_silenty:
                raise
