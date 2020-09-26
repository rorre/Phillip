from typing import Any, Dict, List, Union

import aiohttp
from phillip.application import Phillip
from phillip.osu.new.abstract import ABCClient


class APIClient(ABCClient):
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"

    @property
    def events_url(self):
        return "https://osu.ppy.sh/api/v2/beatmapsets/events?user=&types%5B%5D="

    @property
    def groups_url(self):
        return "https://osu.ppy.sh/groups/"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        client_id: int,
        client_secret: str,
        redirect_uri: str,
        access_token: str,
        refresh_token: str,
        app: Phillip = None,
    ):
        self._app = app
        self._session = session
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self._access_token}"}

    async def _fetch(self, method: str, url: str, data: dict = None) -> dict:
        async with self._session.request(
            method, url, headers=self._headers
        ) as response:
            if response.status == 401:
                await self._fetch_new_token()
                return await self._fetch(method, url)

            response.raise_for_status()
            return await response.json()

    async def _fetch_new_token(self):
        post_data = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token",
        }
        js = await self._fetch("POST", self.TOKEN_URL, data=post_data)
        self._access_token: str = js["access_token"]
        self._refresh_token: str = js["refresh_token"]

    async def get_json(
        self, uri: str, json_tag: str
    ) -> Union[Dict[str, Any], List[dict]]:
        response = await self._fetch("GET", uri)
        json_tag = json_tag[json_tag.find("-") + 1 :]
        return response[json_tag]

