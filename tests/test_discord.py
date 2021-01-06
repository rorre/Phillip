from unittest import mock
from unittest.mock import AsyncMock

import pytest

from phillip.abstract import EventBase
from phillip.application import Phillip
from phillip.discord import DiscordHandler, format_message, gen_embed
from phillip.osu.classes.api import Beatmap
from tests.mocks.discord.mocks import (
    get_api,
    html_mock,
    map_json,
    pop_mock,
    popped_map_json,
)


@pytest.fixture
async def client(event_loop):
    c = Phillip("whatsupslappers", loop=event_loop)
    c.TESTING = True
    yield c
    await c.session.close()


@pytest.fixture
async def event(client: Phillip):
    client.web.get_html = html_mock
    events = [e async for e in client.web.get_events()]
    event = events[0]
    event._beatmap = [Beatmap(j) for j in map_json]
    yield event


@pytest.mark.asyncio
async def test_format():
    result = format_message(
        "04:44:682 - this part is so insanely overdone I don't even know where to start off lmao"
    )
    assert (
        result
        == "04:44:682 - this part is so insanely overdone I don't even know where to start o..."
    )

    multiline_short = format_message("asd\ndsa")
    assert multiline_short == "asd\ndsa"

    multiline_long = format_message(
        "Greetings! This is a veto.\nJust kidding, fix this unsnap."
    )
    assert multiline_long == "Greetings! This is a veto."

    short = format_message("a")
    assert short == "a"


@pytest.mark.asyncio
async def test_embed_ranked(client: Phillip, event: EventBase):
    with mock.patch.object(client.api, "get_api") as mock_object:
        mock_object.side_effect = get_api
        result = await gen_embed(event, client)
        assert result == {
            "title": ":sparkling_heart: Ranked",
            "description": "[**yuikonnu - Souzou Forest**](https://osu.ppy.sh/s/1208022)\r\nMapped by IOException **[osu]**\r\n :thought_balloon: [-Keitaro](https://osu.ppy.sh/u/3378391) :thought_balloon: [Mirash](https://osu.ppy.sh/u/2841009) :heart: [-Keitaro](https://osu.ppy.sh/u/3378391) ",
            "color": 29625,
            "thumbnail": {
                "url": "https://assets.ppy.sh/beatmaps/1208022/covers/list@2x.jpg?1600690662"
            },
        }


@pytest.mark.asyncio
async def test_embed_pop(client: Phillip):
    client.web.get_html = pop_mock
    events = [e async for e in client.web.get_events()]
    event = events[0]
    event._beatmap = [Beatmap(j) for j in popped_map_json]
    with mock.patch.object(client.api, "get_api") as mock_object:
        mock_object.side_effect = get_api
        result = await gen_embed(event, client)
        assert result == {
            "title": ":broken_heart: Disqualified",
            "description": "[**ONE OK ROCK - Start Again**](https://osu.ppy.sh/beatmapsets/beatmap-discussions/1892477)\r\nMapped by Fall **[osu]**",
            "color": 15408128,
            "thumbnail": {
                "url": "https://assets.ppy.sh/beatmaps/1232372/covers/list@2x.jpg?1601338469"
            },
            "footer": {
                "icon_url": "https://a.ppy.sh/3193504",
                "text": "Kibbleru - *This is a veto*\n\nOh man...\n\nHow do I even start here. This map pretty much sums",
            },
        }


@pytest.mark.asyncio
async def test_handler(client: Phillip, event: EventBase):
    h = DiscordHandler("")
    client.add_handler(h)
    with mock.patch.object(client.api, "get_api") as mock_object:
        mock_object.side_effect = get_api
        with mock.patch("aiohttp.ClientSession.post", new_callable=AsyncMock):
            await h.on_map_event(event)
