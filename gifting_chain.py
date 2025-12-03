from __future__ import annotations

from random import shuffle
from random import randint
from typing import override

from user import User


class GiftChain:
    """LinkedList style, GiftChain sends a gifting chain so that each user
    has a unique recipient of gift, and a unique gift deliverable too."""

    hashed_order: str
    assigned: bool

    def __init__(self):
        self.users: list[User] = []
        self.assigned = False

    @override
    def __str__(self) -> str:
        """Hashed output for user output assignment chain"""
        return ' -> '.join(str(user.id) for user in self.users)

    def user_to_str(self) -> str:
        """same thing as __str__, but uses user's name instead (for humans)"""
        return ' -> '.join(user.name for user in self.users)

    def add_user(self, user: User) -> None | tuple(User, User):
        """Adds a user to the GiftChain.
        If not assigned, will return None.
        If assigned, will return tuple of all updated Users.
        """

        # if user is already in GiftChain, overwrite the existing data
        if user in self.users:
            modify_user = self.users[self.users.index(user)]
            if user.interests is not None:
                modify_user.interests = user.interests
            if user.dislikes is not None:
                modify_user.dislikes = user.dislikes

            if modify_user.name != user.name and user.name is not None:
                modify_user.name = user.name

        if not self.assigned:
            self.users.append(user)
            return None

        # at this point, the user will be added to a random index between
        # (and including) 0 to len(users) - 1

        insert_idx = randint(0, len(self.users) - 1)
        updated = []

        # first, update the send_to of the user at the current index.
        previous_user = self.users[insert_idx]
        previous_user.assign(user, previous_user.receive_from)
        updated.append(previous_user)

        # next, update the recieve_from of the next user in the list.
        next_user = self.users[insert_idx + 1]
        next_user.assign(next_user.send_to, user)
        updated.append(next_user)

        # lastly, add the user to the list and assign them
        user.assign(next_user, previous_user)
        self.users.insert(insert_idx, user)

        return tuple(updated)

    def remove_user(self, user: User) -> None | tuple(User, User):
        """ Remove a user from the GiftChain.
        If not assigned, will return None.
        If assigned, will return tuple of all updated Users.

        If you needed to call this method, something has gone wrong.
        NOTE: this operation is irreversible.
        """

        idx_of_user = self.users.index(user)
        updated = []

        previous_user = self.users[idx_of_user - 1]
        next_user = self.users[idx_of_user + 1]

        # first, update the send_to of the user at the current index.
        previous_user.assign(next_user, previous_user.receive_from)
        updated.append(previous_user)

        # next, update the receive_from of the next user in the list.
        next_user.assign(next_user.send_to, previous_user)
        updated.append(next_user)

        self.users.remove(user)

        # deletes old user.
        del user

        return tuple(updated)

    def assign(self):
        """Shuffles the GiftChain, then assigns each user someone to deliver
        the gift to, and one to receive from.

        Note: this operation ideally should only be run once.
        """

        # shuffle the list
        shuffle(self.users)

        for i in range(0, len(self.users) - 1):
            self.users[i].assign(self.users[i - 1], self.users[i + 1])

        # special edge case - last user (to avoid IndexError)
        self.users[-1].assign(self.users[-2], self.users[0])

        self.assigned = True

        if self.assigned:
            raise Warning("The gift chain has already been assigned before")

    @staticmethod
    def create_from_dict(input_dict: dict) -> GiftChain:
        """Creates a new GiftChain from a dictionary."""
        new_chain = GiftChain()
        new_user_list = []

        for user_id in input_dict['users']:
            new_user = User.create_from_dict(user_id, input_dict['users'][user_id])
            new_user_list.append(new_user)

        user_list = input_dict['chain']
        ordered_user_list: list[User] = []
        for user_id in user_list:
            ordered_user_list.append(new_user_list[new_user_list.index(user_id)])

        new_chain.users = ordered_user_list

        return new_chain
