from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Tuple, Type, Union
from urllib.parse import urlencode

import aiohttp

from phillip import abstract, classes
from phillip.osu.classes.web import GroupUser

if TYPE_CHECKING:
    from phillip.application import Phillip


class ABCClient(ABC):
    EVENTS = {
        "nominate": "Bubbled",
        "disqualify": "Disqualified",
        "nomination_reset": "Popped",
    }
    TYPES = ["nominate", "rank", "love", "nomination_reset", "disqualify"]

    def __init__(self, session: aiohttp.ClientSession, app: "Phillip" = None):
        self._app = app
        self._session = session

    @property
    @abstractmethod
    def groups_url(self) -> str:
        pass

    @property
    @abstractmethod
    def events_url(self) -> str:
        pass

    @abstractmethod
    async def get_json(
        self, uri: str, json_tag: str
    ) -> Union[Dict[str, Any], List[dict]]:
        pass

    async def nomination_history(self, mapid: int) -> List[Tuple[str, int]]:
        """Get nomination history of a beatmap. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * mapid - `int` -- Beatmapset ID to gather.

        **Returns**

        * parent - `List[child]` -- A list containing child tuples.
            * `child` - `Tuple[str, int]` -- A tuple with a string of event type and user id of user triggering the event.
        """
        uri = f"https://osu.ppy.sh/beatmapsets/{str(mapid)}/discussion"
        set_json = await self.get_json(uri, "json-beatmapset-discussion")
        js = set_json["beatmapset"]["events"]  # type: ignore

        history = []
        for i, event in enumerate(js):
            if i + 1 != len(js):
                next_event = js[i + 1]
            if event["type"] in self.EVENTS:
                event_name = self.EVENTS[event["type"]]
                if next_event["type"] == "qualify":
                    event_name = "Qualified"
                history.append((event_name, event["user_id"]))
        return history

    async def get_users(self, group_id: int) -> List[GroupUser]:
        """Get users inside of a group. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * group_id - `int` -- The group id.

        **Returns**

        * `List[dict]` -- A dictionary containing users' data.
        """
        uri = self.groups_url + str(group_id)
        users_json = await self.get_json(uri, "json-users")

        out = []
        for user in users_json:
            out.append(GroupUser(user))
        return out

    async def get_events(
        self,
        nominate: bool = True,
        rank: bool = True,
        love: bool = True,
        nomination_reset: bool = True,
        disqualify: bool = True,
        **kwargs,
    ) -> AsyncGenerator[Type[abstract.EventBase], None]:
        """Get events of from osu!website. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * nominate - `bool` -- Whether to get nomination events or not. **This implies `qualify` event.**
        * rank - `bool` -- Whether to get ranked events or not.
        * love - `bool` -- Whetger to get loved events or not.
        * nomination_reset - `bool` -- Whether to get nomination reset events or not.
        * disqualify -- `bool` -- Whether to get disqualification events or not.

        **Yields:**

        * list `abstract.EventBase` -- List of events resulted from fetching osu!web, \
             with next index as next event that will be processed.
        """
        additions = list()
        types_val = [nominate, rank, love, nomination_reset, disqualify]

        for i in range(5):
            additions.append(types_val[i] and self.TYPES[i] or str())
        if types_val[0]:
            additions.append("qualify")
        extras = urlencode(kwargs)
        url = self.events_url + "&types%5B%5D=".join(additions) + "&" + extras

        events = await self.get_json(url, "json-events")
        events.reverse()  # type: ignore

        event_cases = {
            "nominate": classes.Nominated,
            "disqualify": classes.Disqualified,
            "nomination_reset": classes.Popped,
            "rank": classes.Ranked,
            "love": classes.Loved,
        }

        for i, event in enumerate(events):
            action = event["type"]  # type: ignore
            if action == "qualify":
                continue  # Skip qualified event news

            next_map = None
            if i + 1 != len(events):
                next_map = events[i + 1]  # type: ignore

            yield event_cases[action](event, next_map, app=self._app)  # type: ignore
