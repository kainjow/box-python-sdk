# coding: utf-8

from __future__ import unicode_literals

from .box_object_collection import BoxObjectCollection

from typing import Any, Dict, Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..session.session import Session


class MarkerBasedObjectCollection(BoxObjectCollection):
    """
    An iterator of Box objects (BaseObjects) that were retrieved from a Box API endpoint that supports
    marker type of pagination.

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
            marker=None,  # type: Optional[str]
            supports_limit_offset_paging=False,  # type: bool
    ):
        """
        :param marker:
            The offset index to start paging from.
        :param supports_limit_offset_paging:
            Does this particular endpoint also support limit-offset paging? This information is needed, as
            the endpoints that support both require an special extra request parameter.
        """
        super(MarkerBasedObjectCollection, self).__init__(
            session,
            url,
            limit=limit,
            fields=fields,
            additional_params=additional_params,
            return_full_pages=return_full_pages,
        )
        self._marker = marker
        self._supports_limit_offset_paging = supports_limit_offset_paging

    def _update_pointer_to_next_page(self, response_object):
        # type: (Dict[Any, Any]) -> None
        """Baseclass override."""
        self._marker = self._get_next_marker_from_response_object(response_object)

    def _has_more_pages(self, response_object):
        # type: (Dict[Any, Any]) -> bool
        """Baseclass override."""
        return bool(self._get_next_marker_from_response_object(response_object))

    @staticmethod
    def _get_next_marker_from_response_object(response_object):
        # type: (Dict[Any, Any]) -> Optional[str]
        """Get the marker that should be used to retrieve the next page.

        When we've just retrieved the last page, the API is inconsistent about
        what it returns. Some endpoints return "next_marker":"", some return
        "next_marker":null, some don't give any "next_marker" value. In all of
        these cases, this method will return `None`.

        Otherwise, this method returns the string value of the "next_marker"
        field.
        """
        return response_object.get('next_marker') or None

    def _next_page_pointer_params(self):
        # type: () -> Dict[str, object]
        """Baseclass override."""
        pointer_params = {}   # type: Dict[str, object]
        # For transitioning endpoints that support both marker and limit-offset paging, we must specify an
        # additional 'useMarker' parameter to the Box API.
        if self._supports_limit_offset_paging:
            pointer_params['useMarker'] = True
        if self._marker is not None:
            pointer_params['marker'] = self._marker
        return pointer_params

    def next_pointer(self):
        # type: () -> object
        """Baseclass override."""
        return self._marker
