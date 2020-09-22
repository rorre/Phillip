from typing import List

from phillip.abc import EventBase
from phillip.application import Phillip


def has_user(source: dict, target: List[dict]) -> bool:
    """Check if user is inside of another list

    **Parameters:**

    * source - `dict` -- User to be checked.
    * target - `List[dict]` -- List of users that will be compared to.

    **Returns**

    * `bool` -- Boolean value if user is inside another list or not.
    """
    if not target:
        return False

    for user in target:
        if source["id"] == user["id"]:
            return True
    return False
