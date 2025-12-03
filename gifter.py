from __future__ import annotations

from typing import override


class Gifter:
    """
    Represents a gifter for Secret Santa.
    I'm not writing the docstring - you can figure it out.
    """

    def __init__(self, gifter_id: int):

        # General setup
        self.id = gifter_id
        self.name = None
        self.interests = None
        self.dislikes = None

        # Secret Santa purposes
        self.send_to: Gifter = None
        self.receive_from: Gifter = None

    @override
    def __eq__(self, other: Gifter | int | str):
        """Compares gifter_id of gifter"""
        if isinstance(other, Gifter):
            return self.id == other.id
        if isinstance(other, int):
            return self.id == other
        if isinstance(other, str):
            return str(self.id) == other
        return False

    def introduction(self, name: str, interests: str = None, dislikes: str = None) -> None:
        """Note: if you have no interests, you are boring as hell."""
        self.name = name
        self.interests = interests
        self.dislikes = dislikes

    def assign(self, send_to: Gifter, receive_from: Gifter) -> tuple[Gifter, Gifter] | int:
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
    def create_from_dict(gifter_id: int, input_dict: dict) -> Gifter:
        """Create a gifter from a dictionary."""
        new_gifter = Gifter(gifter_id)
        new_gifter.name = input_dict['name']
        new_gifter.interests = input_dict['interests']
        new_gifter.dislikes = input_dict['dislikes']

        return new_gifter
