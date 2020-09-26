from typing import List
from urllib.parse import urlencode

from phillip.osu.classes.api import Beatmap


class APIClient:
    BASE_URL = "https://osu.ppy.sh/api/"

    def __init__(self, session, key):
        self._session = session
        self._key = key

    async def get_api(self, endpoint: str, **kwargs) -> List[dict]:
        """Request something based on endpoint. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Parameters:**

        * endpoint - `str` -- The API endpoint, reference could be found in [osu!wiki](https://github.com/ppy/osu-api/wiki).
        * \*\*kwargs - `dict` | optional -- Keyword arguments that will be passed as a query string.

        **Raises:**

        * `Exception` -- If API key is not assigned.

        **Returns**

        * `List[dict]` -- API response.
        """
        kwargs["k"] = self._key

        api_args = urlencode(kwargs)
        api_url = self.BASE_URL + endpoint + "?" + api_args

        async with self._session.get(api_url) as api_res:
            return await api_res.json()

    async def get_beatmaps(self, **kwargs) -> List[Beatmap]:
        """Get beatmapset from osu! API. *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

        **Returns**

        * `List[Beatmap]` -- Beatmapsets fetched from API.
        """
        return [Beatmap(map) for map in await self.get_api("get_beatmaps", **kwargs)]
