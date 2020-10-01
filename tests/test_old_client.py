import re

import aiohttp
import pytest
from aioresponses import aioresponses

from phillip.osu.old.api import APIClient
from tests.mocks.old_client import MAP_JSONS


@pytest.fixture
async def client(event_loop):
    with aioresponses() as m:
        pattern = re.compile(r"^http[s]://osu\.ppy\.sh.+$")
        m.get(pattern, payload=MAP_JSONS["1068991"])
        c = APIClient(aiohttp.ClientSession(), "whatsupslappers")
        yield c
    await c._session.close()


@pytest.mark.asyncio
async def test_get_maps(client: APIClient):
    assert len(await client.get_beatmaps(s=1068991)) == 1
