# coding: utf-8

from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty
from six import add_metaclass

from typing import Any, Callable, Mapping, Type


@add_metaclass(ABCMeta)
class Network(object):
    """
    Abstract base class specifying the interface of the network layer.
    """

    @abstractmethod
    def request(self, method, url, access_token, **kwargs):
        # type: (str, str, str, **Any) -> NetworkResponse
        """
        Make a network request to the given url with the given method.

        :param method:
            The HTTP verb that should be used to make the request.
        :param url:
            The URL for the request.
        :param access_token:
            The OAuth2 access token used to authorize the request.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def retry_after(self, delay, request_method, *args, **kwargs):
        # type: (float, Callable[..., Any], *Any, **Any) -> NetworkResponse
        """
        Make a network request after a given delay.

        :param delay:
            How long until the request should be executed.
        :param request_method:
            A callable that will execute the request.
        """
        raise NotImplementedError  # pragma: no cover

    @property
    def network_response_constructor(self):
        # type: () -> Type[NetworkResponse]
        """The constructor to use for creating NetworkResponse instances.

        This is not implemented by default, and is not a required part of the
        interface.

        It is recommended that implementations of `request()` call this to
        construct their responses, rather than hard-coding the construction.
        That way, subclasses of the implementation can easily extend the
        construction of :class:`NetworkResponse` instances, by overriding this
        property, instead of needing to override `request()`.

        :return:
            A callable that returns an instance of :class:`NetworkResponse`.
            Most commonly, this will be a subclass of :class:`NetworkResponse`.
        """
        return NetworkResponse


@add_metaclass(ABCMeta)
class NetworkResponse(object):
    """Abstract base class specifying the interface for a network response."""

    @abstractmethod
    def json(self):
        # type: () -> Mapping[Any, Any]
        """Return the parsed JSON response.

        :rtype:
            `dict` or `list` or `str` or `int` or `float`
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def content(self):
        # type: () -> bytes
        """Return the content of the response body.

        :rtype:
            varies
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def status_code(self):
        # type: () -> int
        """Return the HTTP status code of the response.
        """
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def ok(self):
        # type: () -> bool
        """Return whether or not the request was successful.
        """
        # pylint:disable=invalid-name
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def headers(self):
        # type: () -> Mapping[str, str]
        """Return the response headers."""
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def response_as_stream(self):
        # type: () -> Any
        """Return a stream containing the raw network response."""
        raise NotImplementedError  # pragma: no cover

    @abstractproperty
    def access_token_used(self):
        # type: () -> str
        """Return the access token used to make the request."""
        raise NotImplementedError  # pragma: no cover
