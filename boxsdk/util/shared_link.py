# coding: utf-8

from __future__ import unicode_literals

from typing import Dict, Optional


def get_shared_link_header(shared_link, password=None):
    # type: (str, Optional[str]) -> Dict[str, str]
    """
    Gets the HTTP header required to use a shared link to grant access to a shared item.

    :param shared_link:
        The shared link.
    :param password:
        The password for the shared link.
    :return:
        The item referred to by the shared link.
    """
    shared_link_password = '&shared_link_password={0}'.format(password) if password is not None else ''
    box_api_header = 'shared_link={0}{1}'.format(shared_link, shared_link_password)
    return {'BoxApi': box_api_header}
