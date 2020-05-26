# coding: utf-8

from __future__ import unicode_literals, absolute_import

from collections import Sequence
import copy

from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..object.base_object import BaseObject
    from ..session.session import Session
    from ..util.translator import Translator


class Page(Sequence, object):
    """
    A sequence of BaseObjects that belong to a page returned from a paging api call.

    The Page makes available detailed response data for page requests.
    """
    _item_entries_key_name = "entries"

    def __init__(self, session, response_object):
        # type: (Session, Dict[Any, Any]) -> None
        """
        :param session:
            The Box session used to make the request that generated the response.
        :param response_object:
            The parsed HTTP response from Box after requesting more pages.
        :type response_object:
            `dict`
        """
        super(Page, self).__init__()
        self._session = session
        self._response_object = response_object

    @property
    def _translator(self):
        # type: () -> Translator
        """The translator used for translating Box API JSON responses into `BaseAPIJSONObject` smart objects.
        """
        return self._session.translator

    @property
    def response_object(self):
        # type: () -> Dict[Any, Any]
        """
        Return a copy of the response object for this Page.
        """
        return copy.deepcopy(self._response_object)

    def __getitem__(self, key):  # type: ignore[override]
        # type: (str) -> object
        """
        Try to get the attribute from the API response object.

        :param key:
            The attribute to retrieve from the API response object.
        :rtype:
            :class:`BaseObject`
        """
        item_json = self._response_object[self._item_entries_key_name][key]
        return self._translator.translate(self._session, item_json)

    def __len__(self):
        # type: () -> int
        """
        Get the number of items in the page.
        """
        return len(self._response_object[self._item_entries_key_name])
