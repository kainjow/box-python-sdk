# coding: utf-8

from __future__ import unicode_literals, absolute_import

import attr

from ..util.log import sanitize_dictionary

from typing import Dict


@attr.s(slots=True)
class BoxRequest(object):
    """Represents a Box API request.

    :param url:                     The URL being requested.
    :param method:                  The HTTP method to use for the request.
    :param headers:                 HTTP headers to include with the request.
    :param auto_session_renewal:    Whether or not the session can be automatically renewed if the request fails.
    :param expect_json_response:    Whether or not the API response must be JSON.
    """
    url = attr.ib()  # type: str
    method = attr.ib(default='GET')  # type: str
    headers = attr.ib(default=attr.Factory(dict))  # type: Dict[str, str]
    auto_session_renewal = attr.ib(default=True)  # type: bool
    expect_json_response = attr.ib(default=True)  # type: bool

    def __repr__(self):
        # type: () -> str
        return '<BoxRequest for {self.method} {self.url} with headers {headers}'.format(
            self=self,
            headers=sanitize_dictionary(self.headers),
        )
