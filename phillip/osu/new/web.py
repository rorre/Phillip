import json
from typing import Any, Dict, List, Union

from asyncio_throttle import Throttler
from bs4 import BeautifulSoup

from phillip.osu.new.abstract import ABCClient


class WebClient(ABCClient):
    @property
    def events_url(self):
        return "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D="

    @property
    def groups_url(self):
        return "https://osu.ppy.sh/groups/"

    def __init__(self, session, throttler=None, app=None):
        super().__init__(session, app)
        self._throttler = throttler or Throttler(rate_limit=2, period=60)

    async def get_html(self, uri: str) -> BeautifulSoup:
        """Receive html from uri with rate limit.
        *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * uri - `str` -- URL of discussion page.

        **Returns**

        * BeautifulSoup -- Soup'd html response.
        """
        async with self._throttler:
            async with self._session.get(uri, cookies={"locale": "en"}) as site_html:
                return BeautifulSoup(await site_html.text(), features="html.parser")

    async def get_json(
        self, uri: str, json_tag: str
    ) -> Union[Dict[str, Any], List[dict]]:
        soup = await self.get_html(uri)
        js_str = soup.find(id=json_tag).string
        return json.loads(js_str)
