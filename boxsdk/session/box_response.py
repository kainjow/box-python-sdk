# coding: utf-8

from __future__ import unicode_literals, absolute_import

from typing import Any, Dict, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from ..network.network_interface import NetworkResponse


class BoxResponse(object):
    """Represents a response to a Box API request."""

    def __init__(self, network_response):
        # type: (NetworkResponse) -> None
        self._network_response = network_response

    def json(self):
        # type: () -> Dict[Any, Any]
        """Return the parsed JSON response.

        :rtype:
            `dict` or `list` or `str` or `int` or `float`
        """
        return self._network_response.json()

    @property
    def content(self):
        # type: () -> bytes
        """Return the content of the response body.

        :rtype:
            varies
        """
        return self._network_response.content

    @property
    def ok(self):
        # type: () -> bool
        """Return whether or not the request was successful.
        """
        # pylint:disable=invalid-name
        return self._network_response.ok

    @property
    def status_code(self):
        # type: () -> int
        """Return the HTTP status code of the response.
        """
        return self._network_response.status_code

    @property
    def headers(self):
        # type: () -> Mapping[str, str]
        """
        Get the response headers.
        """
        return self._network_response.headers

    @property
    def network_response(self):
        # type: () -> NetworkResponse
        """Return the underlying network response.
        """
        return self._network_response

    def __repr__(self):
        # type: () -> str
        return '<Box Response[{status_code}]>'.format(status_code=self.status_code)
