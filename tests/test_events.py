from datetime import datetime
from typing import List, Type
from unittest import mock

import pytest

from phillip.abstract import EventBase
from phillip.application import Phillip
from phillip.classes import Disqualified, Loved, Nominated, Popped, Ranked
from phillip.osu.classes.web import Discussion, Post
from tests.mocks.new_client import html_mock
from tests.mocks.old_client import get_api


@pytest.fixture
async def client(event_loop):
    app = Phillip("pog")
    yield app
    await app.session.close()


@pytest.fixture
async def events(client: Phillip):
    client.web.get_html = html_mock
    events = [e async for e in client.web.get_events()]
    yield events


def test_gamemodes_except():
    with pytest.raises(Exception):
        Ranked({}).gamemodes


@pytest.mark.asyncio
async def test_abstract(client: Phillip, events: List[Type[EventBase]]):
    event: Ranked = events[-1]
    with mock.patch.object(client.api, "get_api") as mock_object:
        mock_object.side_effect = get_api
        await event.get_beatmap()

    assert event.artist == "Doja Cat"
    assert event.creator == "Plaudible"
    assert event.gamemodes == ["osu"]
    assert (
        event.map_cover
        == "https://assets.ppy.sh/beatmaps/1107500/covers/list@2x.jpg?1600644042"
    )
    assert event.time == datetime.strptime(
        "2020-09-29T07:43:31+00:00", "%Y-%m-%dT%H:%M:%S+00:00"
    )
    assert event.title == "Boss Bitch"


def test_ranked(client: Phillip, events: List[Type[EventBase]]):
    event: Ranked = events[-1]
    assert event.event_type == "Ranked"


def test_loved(client: Phillip, events: List[Type[EventBase]]):
    event: Loved = events[0]
    assert event.event_type == "Loved"


def test_nominated(client: Phillip, events: List[Type[EventBase]]):
    event: Nominated = events[9]
    assert event.event_type == "Bubbled"
    assert event.user_id == 9327302


def test_qualified(client: Phillip, events: List[Type[EventBase]]):
    event: Nominated = events[10]
    assert event.event_type == "Qualified"


def test_reset(client: Phillip, events: List[Type[EventBase]]):
    event: Popped = events[7]
    assert event.event_type == "Popped"
    assert (
        event.event_source_url
        == "https://osu.ppy.sh/beatmapsets/beatmap-discussions/1892746"
    )


def test_disqualify(client: Phillip, events: List[Type[EventBase]]):
    event: Disqualified = events[5]
    assert event.event_type == "Disqualified"


def test_discussion(events: List[Type[EventBase]]):
    event: Disqualified = events[5]
    discussion: Discussion = event.discussion
    assert discussion.id == 1892477
    assert discussion.beatmapset_id == 1232372
    assert discussion.beatmap_id is None
    assert discussion.user_id == 3193504
    assert discussion.deleted_by_id is None
    assert discussion.message_type == "problem"
    assert discussion.parent_id is None
    assert discussion.timestamp is None
    assert not discussion.resolved
    assert discussion.can_be_resolved
    assert discussion.can_grant_kudosu
    assert discussion.created_at == "2020-09-28T21:49:08+00:00"
    assert discussion.updated_at == "2020-09-29T01:43:16+00:00"
    assert discussion.deleted_at is None
    assert discussion.last_post_at == "2020-09-29T01:43:16+00:00"
    assert not discussion.kudosu_denied
    assert type(discussion.starting_post) == Post


def test_post(events: List[Type[EventBase]]):
    event: Disqualified = events[5]
    post: Post = event.discussion.starting_post
    assert post.id == 5290246
    assert post.beatmap_discussion_id == 1892477
    assert post.user_id == 3193504
    assert post.last_editor_id is None
    assert post.deleted_by_id is None
    assert not post.system
    assert "veto" in post.message
    assert post.created_at == "2020-09-28T21:49:08+00:00"
    assert post.updated_at == "2020-09-28T21:49:08+00:00"
    assert not post.deleted_at


def test_no_discussion(events: List[Type[EventBase]]):
    event: Ranked = events[-1]
    assert event.discussion is None
