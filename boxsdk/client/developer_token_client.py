# coding: utf-8

from __future__ import unicode_literals, absolute_import

from ..auth import DeveloperTokenAuth
from .client import Client

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..auth.oauth2 import OAuth2
    from ..session.session import Session


class DeveloperTokenClient(Client):
    """
    Box client subclass which authorizes with a developer token.
    """
    def __init__(self, oauth=None, session=None):
        # type: (Optional[OAuth2], Optional[Session]) -> None
        super(DeveloperTokenClient, self).__init__(
            oauth=oauth or DeveloperTokenAuth(),
            session=session,
        )
