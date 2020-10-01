import re

import aiohttp
import pytest
from aioresponses import aioresponses
from asyncio_throttle import Throttler

from phillip.osu.new.web import WebClient
from tests.mocks.new_client import html_text


@pytest.fixture
async def client(event_loop):
    with aioresponses() as m:
        pattern = re.compile(r"^https://osu\.ppy\.sh.+$")
        m.get(pattern, body=html_text, repeat=True, content_type="text/html")
        c = WebClient(aiohttp.ClientSession(), Throttler(rate_limit=9999, period=60))
        yield c
    await c._session.close()


@pytest.mark.asyncio
async def test_get(client: WebClient):
    assert len([e async for e in client.get_events()]) == 18
    assert len(await client.get_users(28)) == 94
    assert await client.nomination_history(1205309) == [
        ("Bubbled", 4800816),
        ("Qualified", 4446810),
    ]
