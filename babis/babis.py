# -*- coding: utf-8 -*-
import six
from six.moves.urllib.request import Request, urlopen
from six.moves.urllib.error import URLError


class decorator(object):
    def __init__(self, ping_before=None, ping_after=None, fail_silenty=False,
                 method='GET', user_agent='curl/7.50.1'):
        self.ping_before = ping_before
        self.ping_after = ping_after
        self.fail_silenty = fail_silenty
        self.method = method
        self.user_agent = user_agent

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            if self.ping_before:
                self.ping_urls(self.ping_before)
            fn(*args, **kwargs)
            if self.ping_after:
                self.ping_urls(self.ping_after)
        return wrapped

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
