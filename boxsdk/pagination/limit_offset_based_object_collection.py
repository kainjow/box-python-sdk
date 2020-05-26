# coding: utf-8

from __future__ import unicode_literals

from .box_object_collection import BoxObjectCollection

from typing import Any, Dict, Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..session.session import Session


class LimitOffsetBasedObjectCollection(BoxObjectCollection):
    """
    An iterator of Box objects (BaseObjects) that were retrieved from a Box API endpoint that supports
    limit-offset type of pagination.

    See https://developer.box.com/en/guides/api-calls/pagination/ for more details.
    """

    def __init__(
            self,
            session,  # type: Session
            url,  # type: str
            limit=None,  # type: Optional[int]
            fields=None,  # type: Optional[Iterable[str]]
            additional_params=None,  # type: Optional[Dict[Any, Any]]
            return_full_pages=False,  # type: bool
            offset=0,  # type: Optional[int]
    ):  # type: (...) -> None
        """
        :param offset:
            The offset index to start paging from.
        """
        super(LimitOffsetBasedObjectCollection, self).__init__(
            session,
            url,
            limit=limit,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=return_full_pages,
        )
        self._offset = offset

    def _update_pointer_to_next_page(self, response_object):
        # type: (Dict[Any, Any]) -> None
        """Baseclass override."""
        total_count = response_object['total_count']

        if 'limit' in response_object:
            self._limit, old_limit = int(response_object['limit']), self._limit

            # The API might use a lower limit than the client asked for, if the
            # client asked for a limit above the maximum limit for that endpoint.
            # The API is supposed to respond with the limit that it actually used.
            # If that is given, then use that limit for the offset calculation, and
            # also for the remainder of the paging.

            # Do not apply this same logic to "offset". Offset is not documented to be
            # changed in the response, so respecting that value can lead to undefined
            # behavior.

            # If the API erroneously sends a bad value for limit, we want to
            # avoid getting into an infinite chain of API calls. So abort with
            # a runtime error.
            if self._limit <= 0 < old_limit:
                self._offset = total_count  # Disable additional paging.
                raise RuntimeError('API returned limit={0}, cannot continue paging'.format(self._limit))

        # de-none-ify the _offset value so that the arthimatic below works
        self._offset = self._offset or 0
        limit = self._limit or 0

        if total_count >= self._offset + limit:
            self._offset += limit
        else:
            self._offset = total_count

    def _has_more_pages(self, response_object):
        # type: (Dict[Any, Any]) -> bool
        """Baseclass override."""
        return self._offset < response_object['total_count']

    def _next_page_pointer_params(self):
        # type: () -> Dict[str, object]
        """Baseclass override."""
        return {'offset': self._offset}

    def next_pointer(self):
        # type: () -> object
        """Baseclass override."""
        return self._offset
