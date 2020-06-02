import json
from typing import Generator, List, Tuple
from urllib.parse import urlencode

from asyncio_throttle import Throttler
from bs4 import BeautifulSoup

from phillip import abc, classes
from phillip.osu.classes.web import GroupUser


class WebClient:
    BASE_GROUPS_URL = "https://osu.ppy.sh/groups/"
    EVENTS = {
        "nominate": "Bubbled",
        "disqualify": "Disqualified",
        "nomination_reset": "Popped",
    }
    BASE_EVENTS_URL = "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D="
    TYPES = ["nominate", "rank", "love", "nomination_reset", "disqualify"]

    def __init__(self, session, throttler=None, app=None):
        self._app = app
        self._session = session
        self._throttler = throttler or Throttler(rate_limit=2, period=60)

    async def get_html(self, uri: str) -> BeautifulSoup:
        """Receive html from uri. 
        *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * uri - `str` -- URL of discussion page.

        **Returns**

        * BeautifulSoup -- Soup'd html response.
        """
        async with self._throttler:
            async with self._session.get(uri, cookies={"locale": "en"}) as site_html:
                return BeautifulSoup(await site_html.text(), features="html.parser")

    async def get_discussion_json(self, uri: str) -> List[dict]:
        """Receive discussion posts in JSON. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * uri - `str` -- URL of discussion page.

        **Returns**

        * `List[dict]` -- The discussion posts.
        """

        soup = await self.get_html(uri)
        set_json_str = soup.find(id="json-beatmapset-discussion").text
        set_json = json.loads(set_json_str)
        return set_json["beatmapset"]["discussions"]

    async def nomination_history(self, mapid: int) -> List[Tuple[str, int]]:
        """Get nomination history of a beatmap. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * mapid - `int` -- Beatmapset ID to gather.

        **Returns**

        * parent - `List[child]` -- A list containing child tuples.
            * `child` - `Tuple[str, int]` -- A tuple with a string of event type and user id of user triggering the event.
        """
        uri = f"https://osu.ppy.sh/beatmapsets/{str(mapid)}/discussion"
        soup = await self.get_html(uri)
        set_json_str = soup.find(id="json-beatmapset-discussion").text
        set_json = json.loads(set_json_str)
        js = set_json["beatmapset"]["events"]

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

    async def get_users(self, group_id: int) -> List[dict]:
        """Get users inside of a group. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * group_id - `int` -- The group id.

        **Returns**

        * `List[dict]` -- A dictionary containing users' data.
        """
        uri = self.BASE_GROUPS_URL + str(group_id)
        bs = await self.get_html(uri)
        users_tag = bs.find(id="json-users").text
        users_json = json.loads(users_tag)

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
    ) -> Generator[List[abc.EventBase], None, None]:
        """Get events of from osu!website. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * nominate - `bool` -- Whether to get nomination events or not. **This implies `qualify` event.**
        * rank - `bool` -- Whether to get ranked events or not.
        * love - `bool` -- Whetger to get loved events or not.
        * nomination_reset - `bool` -- Whether to get nomination reset events or not.
        * disqualify -- `bool` -- Whether to get disqualification events or not.

        **Yields:**

        * list `abc.EventBase` -- List of events resulted from fetching osu!web, \
             with next index as next event that will be processed.
        """
        additions = list()
        types_val = [nominate, rank, love, nomination_reset, disqualify]

        for i in range(5):
            additions.append(types_val[i] and self.TYPES[i] or str())
        if types_val[0]:
            additions.append("qualify")
        extras = urlencode(kwargs)
        url = self.BASE_EVENTS_URL + "&types%5B%5D=".join(additions) + "&" + extras

        res_soup = await self.get_html(url)
        events_html = res_soup.find(id="json-events").text
        events = json.loads(events_html)
        events.reverse()

        event_cases = {
            "nominate": classes.Nominated,
            "disqualify": classes.Disqualified,
            "nomination_reset": classes.Popped,
            "rank": classes.Ranked,
            "love": classes.Loved,
        }

        for i, event in enumerate(events):
            action = event["type"]
            if action == "qualify":
                continue  # Skip qualified event news

            next_map = None
            if i + 1 != len(events):
                next_map = events[i + 1]

            yield event_cases[action](event, next_map, app=self._app)
