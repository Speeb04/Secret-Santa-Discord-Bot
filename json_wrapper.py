from __future__ import annotations

import json
from typing import final

from gifting_chain import GiftChain

@final
class JSONWrapper:
    """
    Wrapper class which takes a GiftChain object and converts it to a JSON file.
    """

    @staticmethod
    def convert_to_dict(gift_chain: GiftChain) -> dict:
        """
        Converts a GiftChain object to a dictionary with primitive datatypes.
        :param gift_chain:
        :return dict:
        """

        output_dict = {"chain": [gifter.id for gifter in gift_chain.gifters], "gifters": {}, "assigned": gift_chain.assigned}

        for gifter in gift_chain.gifters:
            if gifter.send_to is None and gifter.receive_from is None:
                output_dict["gifters"][gifter.id] = {
                    "name": gifter.name,
                    "interests": gifter.interests,
                    "dislikes": gifter.dislikes,
                    "send_to": gifter.send_to,
                    "receive_from": gifter.receive_from
                }
            else:
                output_dict["gifters"][gifter.id] = {
                    "name": gifter.name,
                    "interests": gifter.interests,
                    "dislikes": gifter.dislikes,
                    "send_to": gifter.send_to.id,
                    "receive_from": gifter.receive_from.id
                }

        return output_dict

    @staticmethod
    def write_to_file(gift_chain: GiftChain, filename: str = "giftchain.json") -> None:
        with open(filename, "w") as file:
            json.dump(JSONWrapper.convert_to_dict(gift_chain), file, indent=4)

    @staticmethod
    def read_from_file(filename: str = "giftchain.json") -> GiftChain:
        with open(filename, "r") as file:
            input_dict = json.load(file)
            return GiftChain.create_from_dict(input_dict)



