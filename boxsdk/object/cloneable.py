# coding: utf-8

from __future__ import unicode_literals, absolute_import

from typing import Optional, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    T = TypeVar('T', bound='Cloneable')

    from .user import User
    from ..session.session import Session


class Cloneable(object):
    """
    Cloneable interface to be implemented by endpoint objects that should have ability to be cloned, but with a
    different session member if desired.
    """

    def as_user(self, user):
        # type: (T, User) -> T
        """
        Returns a new endpoint object with default headers set up to make requests as the specified user.

        :param user:
            The user to impersonate when making API requests.
        """
        return self.clone(self.session.as_user(user))

    def with_shared_link(self, shared_link, shared_link_password):
        # type: (T, str, Optional[str]) -> T
        """
        Returns a new endpoint object with default headers set up to make requests using the shared link for auth.

        :param shared_link:
            The shared link.
        :param shared_link_password:
            The password for the shared link.
        """
        return self.clone(self.session.with_shared_link(shared_link, shared_link_password))

    def clone(self, session=None):
        # type: (T, Optional[Session]) -> T
        """
        Returns a copy of this cloneable object using the specified session.

        :param session:
            The Box session used to make requests.
        :type session:
            :class:`BoxSession`
        """
        raise NotImplementedError

    @property
    def session(self):
        # type: () -> Session
        """
        Return the Box session being used to make requests.
        """
        raise NotImplementedError
