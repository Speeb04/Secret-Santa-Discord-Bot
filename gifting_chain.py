from __future__ import annotations

from random import shuffle
from random import randint
from typing import override

from gifter import Gifter


class GiftChain:
    """LinkedList style, GiftChain sends a gifting chain so that each gifter
    has a unique recipient of gift, and a unique gift deliverable too."""

    hashed_order: str
    assigned: bool
    gifters: list[Gifter] = []
    assigned = False

    @override
    def __str__(self) -> str:
        """Hashed output for gifter output assignment chain"""
        return ' -> '.join(str(gifter.id) for gifter in self.gifters)

    def gifter_to_str(self) -> str:
        """same thing as __str__, but uses gifter's name instead (for humans)"""
        return ' -> '.join(gifter.name for gifter in self.gifters)

    def get_gifter_by_id(self, id: int) -> Gifter | None:
        """Returns a gifter in Giftchain.gifters by ID, or None if not found"""
        for gifter in self.gifters:
            if gifter.id == id:
                return gifter
        return None

    def add_gifter(self, gifter: Gifter) -> None | tuple(Gifter, Gifter):
        """Adds a gifter to the GiftChain.
        If not assigned, will return None.
        If assigned, will return tuple of all updated gifters.
        """

        # if gifter is already in GiftChain, overwrite the existing data
        if gifter in self.gifters:
            modify_gifter = self.gifters[self.gifters.index(gifter)]
            if gifter.interests is not None:
                modify_gifter.interests = gifter.interests
            if gifter.dislikes is not None:
                modify_gifter.dislikes = gifter.dislikes

            if modify_gifter.name != gifter.name and gifter.name is not None:
                modify_gifter.name = gifter.name

            return None

        if not self.assigned:
            self.gifters.append(gifter)
            return None

        # at this point, the gifter will be added to a random index between
        # (and including) 0 to len(gifters) - 1

        insert_idx = randint(0, len(self.gifters) - 1)
        updated = []

        # first, update the send_to of the gifter at the current index.
        previous_gifter = self.gifters[insert_idx]
        previous_gifter.assign(gifter, previous_gifter.receive_from)
        updated.append(previous_gifter)

        # next, update the recieve_from of the next gifter in the list.
        next_gifter = self.gifters[insert_idx + 1]
        next_gifter.assign(next_gifter.send_to, gifter)
        updated.append(next_gifter)

        # lastly, add the gifter to the list and assign them
        gifter.assign(next_gifter, previous_gifter)
        self.gifters.insert(insert_idx, gifter)

        return tuple(updated)

    def remove_gifter(self, gifter: Gifter) -> None | tuple(Gifter, Gifter):
        """ Remove a gifter from the GiftChain.
        If not assigned, will return None.
        If assigned, will return tuple of all updated gifters.

        If you needed to call this method, something has gone wrong.
        NOTE: this operation is irreversible.
        """

        idx_of_gifter = self.gifters.index(gifter)
        updated = []

        previous_gifter = self.gifters[idx_of_gifter - 1]
        next_gifter = self.gifters[idx_of_gifter + 1]

        # first, update the send_to of the gifter at the current index.
        previous_gifter.assign(next_gifter, previous_gifter.receive_from)
        updated.append(previous_gifter)

        # next, update the receive_from of the next gifter in the list.
        next_gifter.assign(next_gifter.send_to, previous_gifter)
        updated.append(next_gifter)

        self.gifters.remove(gifter)

        # deletes old gifter.
        del gifter

        return tuple(updated)

    def assign(self):
        """Shuffles the GiftChain, then assigns each gifter someone to deliver
        the gift to, and one to receive from.

        Note: this operation ideally should only be run once.
        """

        if self.assigned:
            raise Warning("The gift chain has already been assigned before")

        # shuffle the list
        shuffle(self.gifters)

        for i in range(0, len(self.gifters) - 1):
            self.gifters[i].assign(self.gifters[i + 1], self.gifters[i - 1])

        # special edge case - last gifter (to avoid IndexError)
        self.gifters[-1].assign(self.gifters[0], self.gifters[-2])

        self.assigned = True

    @staticmethod
    def create_from_dict(input_dict: dict) -> GiftChain:
        """Creates a new GiftChain from a dictionary."""
        new_chain = GiftChain()
        new_gifter_list = []

        new_chain.assigned = input_dict["assigned"]

        for gifter_id in input_dict['gifters']:
            new_gifter = Gifter.create_from_dict(int(gifter_id), input_dict['gifters'][gifter_id])
            new_gifter_list.append(new_gifter)

        gifter_list = input_dict['chain']
        ordered_gifter_list: list[Gifter] = []
        for gifter_id in gifter_list:
            for new_gifter in new_gifter_list:
                if new_gifter.id == gifter_id:
                    ordered_gifter_list.append(new_gifter)

        # So far, gifters are unassigned.
        # Let's fix that.
        if new_chain.assigned:
            for gifter in new_chain.gifters:
                send_to_index = input_dict['gifters'][str(gifter.id)]['send_to']
                receive_from_index = input_dict['gifters'][str(gifter.id)]['receive_from']
                gifter.assign(new_chain.get_gifter_by_id(send_to_index), new_chain.get_gifter_by_id(receive_from_index))

        new_chain.gifters = ordered_gifter_list

        return new_chain
