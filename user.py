from __future__ import annotations

from typing import override


class User:
    """
    Represents a user for Secret Santa.
    I'm not writing the docstring - you can figure it out.
    """

    def __init__(self, user_id: int):

        # General setup
        self.id = user_id
        self.name = None
        self.interests = None
        self.dislikes = None

        # Secret Santa purposes
        self.send_to: User = None
        self.receive_from: User = None

    @override
    def __eq__(self, other: User):
        """Compares user_id of User"""
        return self.id == other.id

    def introduction(self, name: str, interests: str = None, dislikes: str = None) -> None:
        """Note: if you have no interests, you are boring as hell."""
        self.name = name
        self.interests = interests
        self.dislikes = dislikes

    def assign(self, send_to: User, receive_from: User) -> tuple[User, User] | int:
        """Assign someone to send a gift to, and one to receive a gift from.
        Note that if either parameter is None or empty, it will throw an IOError.

        Returns previous value in the form of (send to, receive from).
        If previous send_to and receive_from are None, returns -1.
        """

        assert ((self.send_to is None and self.receive_from is None) |
                (self.send_to is not None and self.receive_from is not None)), (
            "If you see this, something has gone very wrong. send_to and "
            "receive_from must either both be or neither is None.")

        if send_to is None or receive_from is None:
            raise IOError("send_to and receive_from are not defined.")

        if send_to == self or receive_from == self:
            raise IOError("Cannot send to or receive gift from self.")

        previous_send_to = self.send_to
        previous_receive_from = self.receive_from

        self.send_to = send_to
        self.receive_from = receive_from

        if previous_send_to is None and previous_receive_from is None:
            return -1

        return previous_send_to, previous_receive_from

    @staticmethod
    def create_from_dict(user_id: int, input_dict: dict) -> User:
        """Create a User from a dictionary."""
        new_user = User(user_id)
        new_user.name = input_dict['name']
        new_user.interests = input_dict['interests']
        new_user.dislikes = input_dict['dislikes']
        new_user.send_to = input_dict['send_to']
        new_user.receive_from = input_dict['receive_from']

        return new_user
