from __future__ import annotations

import json
from typing import final

from gifting_chain import GiftChain
from user import User

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

        if not gift_chain.assigned:
            raise AttributeError("GiftChain object has not been assigned.")

        output_dict = {"chain": [user.id for user in gift_chain.users], "users": {}}

        for user in gift_chain.users:
            output_dict["users"][user.id] = {
                "name": user.name,
                "interests": user.interests,
                "dislikes": user.dislikes,
                "send_to": user.send_to,
                "receive_from": user.receive_from
            }

        return output_dict

    @staticmethod
    def write_to_file(GiftChain: GiftChain, filename: str = "giftchain.json") -> None:
        with open(filename, "w") as file:
            json.dump(JSONWrapper.convert_to_dict(GiftChain), file)

    @staticmethod
    def read_from_file(filename: str = "giftchain.json") -> GiftChain:
        with open(filename, "r") as file:
            input_dict = JSONWrapper.convert_to_dict(json.load(file))
            return GiftChain.create_from_dict(input_dict)



