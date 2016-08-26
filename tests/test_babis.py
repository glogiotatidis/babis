#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_babis
----------------------------------

Tests for `babis` module.
"""

import pytest
from mock import ANY, Mock, call, patch
from six.moves.urllib.error import URLError


from babis import decorator


class TestBabis(object):
    def test_before_and_after(self):
        first_request = Mock()
        second_request = Mock()
        third_request = Mock()

        with patch('babis.babis.Request') as Request:
            Request.side_effect = [
                first_request,
                third_request
            ]
            with patch('babis.babis.urlopen') as urlopen:
                def wrapped():
                    urlopen(second_request)
                decorator(ping_before='foo', ping_after='bar')(wrapped)()

        urlopen.assert_has_calls([
            call(first_request), call(second_request), call(third_request)])

    def test_ping_urls_string(self):
        dec = decorator()
        dec.ping_url = Mock()
        dec.ping_urls('foo')
        dec.ping_url.assert_called_with('foo')

    def test_ping_urls_iterable(self):
        dec = decorator()
        dec.ping_url = Mock()
        dec.ping_urls(('foo', 'bar'))
        dec.ping_url.assert_has_calls([call('foo'), call('bar')])

    def test_ping_url(self):
        dec = decorator()
        with patch('babis.babis.Request') as Request:
            request_init_mock = Mock()
            Request.return_value = request_init_mock
            with patch('babis.babis.urlopen') as urlopen:
                dec.ping_url('foo')
        Request.assert_called_with('foo', data=ANY, headers=ANY)
        urlopen.assert_called_with(request_init_mock)

    def test_user_agent(self):
        dec = decorator(user_agent='foo')
        with patch('babis.babis.Request') as Request:
            with patch('babis.babis.urlopen'):
                dec.ping_url('foo')
        Request.assert_called_with(ANY, data=ANY, headers={'User-Agent': 'foo'})

    def test_method(self):
        dec = decorator(method='post')
        with patch('babis.babis.Request') as Request:
            with patch('babis.babis.urlopen'):
                dec.ping_url('foo')
        Request.assert_called_with(ANY, data='', headers=ANY)

    def test_fail_silenty_false(self):
        dec = decorator(fail_silenty=False)
        with patch('babis.babis.Request') as Request:
            with patch('babis.babis.urlopen') as urlopen:
                urlopen.side_effect = URLError('Boom!')
                with pytest.raises(URLError):
                    dec.ping_url('foo')

    def test_fail_silenty_true(self):
        dec = decorator(fail_silenty=True)
        with patch('babis.babis.Request') as Request:
            with patch('babis.babis.urlopen') as urlopen:
                urlopen.side_effect = URLError('Boom!')
                dec.ping_url('foo')
