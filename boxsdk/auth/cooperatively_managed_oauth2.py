# coding: utf-8

from __future__ import unicode_literals
from .oauth2 import OAuth2

from typing import Any, Callable, Optional, Tuple


class CooperativelyManagedOAuth2Mixin(OAuth2):
    """
    Box SDK OAuth2 mixin.
    Allows for sharing auth tokens between multiple clients.
    """
    def __init__(self, retrieve_tokens=None, *args, **kwargs):
        # type: (Callable[[], Tuple[str, str]], *Any, **Any) -> None
        """
        :param retrieve_tokens:
            Callback to get the current access/refresh token pair.
        :type retrieve_tokens:
            `callable` of () => (`unicode`, `unicode`)
        """
        # pylint:disable=keyword-arg-before-vararg
        self._retrieve_tokens = retrieve_tokens
        super(CooperativelyManagedOAuth2Mixin, self).__init__(*args, **kwargs)

    def _get_tokens(self):
        # type: () -> Tuple[Optional[str], Optional[str]]
        """
        Base class override. Get the tokens from the user-specified callback.
        """
        assert self._retrieve_tokens is not None  # for mypy
        return self._retrieve_tokens()


class CooperativelyManagedOAuth2(CooperativelyManagedOAuth2Mixin):
    """
    Box SDK OAuth2 subclass.
    Allows for sharing auth tokens between multiple clients. The retrieve_tokens callback should
    return the current access/refresh token pair.
    """
    pass
