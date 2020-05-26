# coding: utf-8

from __future__ import unicode_literals, absolute_import

from .client import Client
from ..util.log import setup_logging

from typing import Any


class LoggingClient(Client):
    """
    Box client subclass which logs requests and responses.
    """
    def __init__(self, *args, **kwargs):
        # type: (*Any, **Any) -> None
        setup_logging(None)
        super(LoggingClient, self).__init__(*args, **kwargs)
