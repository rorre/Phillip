import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from phillip.abstract import EventBase
from phillip.application import Phillip
from phillip.handlers import Handler
from phillip.osu.classes.web import GroupUser
from tests.mocks.application import (api_mock, bancho_event_mock, events_mock,
                                     users_mock)


@pytest.fixture
async def client(event_loop):
    c = Phillip("whatsupslappers", loop=event_loop)
    c.TESTING = True
    yield c
    await c.session.close()


@pytest.mark.asyncio
async def test_handler_register():
    h = Handler()
    p = Phillip("", handlers=[h])

    assert h.emitter is not None
    assert h.app == p


@pytest.mark.asyncio
async def test_start(client: Phillip):
    # No handler or webhook url
    with pytest.raises(Exception):
        client.run()

    client.webhook_url = "yes"
    client.run()
    assert len(client.tasks) == 2

    for task in client.tasks:
        task.cancel()


@pytest.mark.asyncio
async def test_add_handler(client: Phillip):
    class SampleHandler(Handler):
        pass

    client.add_handler(SampleHandler())


@pytest.mark.asyncio
async def test_mapfeed(client: Phillip):
    client.web.get_json = events_mock
    client.api.get_api = api_mock

    class TestHandler(Handler):
        working = False

        async def on_map_event(self, event: EventBase):
            self.working = True

    # Normal work
    h = TestHandler()
    client.handlers = []
    client.add_handler(h)
    await asyncio.wait_for(client.check_map_events(), 5)
    assert h.working

    # Check if current event is before last event
    h.working = False
    client.last_date = datetime.max
    await asyncio.wait_for(client.check_map_events(), 5)
    assert not h.working

    # Duplicate event
    h.working = False
    client.last_date = datetime.strptime(
        "2020-09-29T07:43:31+00:00", "%Y-%m-%dT%H:%M:%S+00:00"
    )
    await asyncio.wait_for(client.check_map_events(), 5)
    assert not h.working

    # Bancho skipping
    client.web.get_json = bancho_event_mock

    h.working = False
    client.last_date = datetime.min
    await asyncio.wait_for(client.check_map_events(), 5)
    assert not h.working


@pytest.mark.asyncio
async def test_mapfeed_on_error(capsys, client: Phillip):
    # TypeError would happen as its not an async generator
    client.web.get_events = Mock()
    await client.check_map_events()
    _, err = capsys.readouterr()
    assert "TypeError" in err


@pytest.mark.asyncio
async def test_groupfeed(client: Phillip):
    class TestUserHandler(Handler):
        add_working = False
        remove_working = False

        async def on_group_added(self, user: GroupUser):
            self.add_working = True

        async def on_group_removed(self, user: GroupUser):
            self.remove_working = True

    client.group_ids = [28]
    client.web.get_json = users_mock

    h = TestUserHandler()
    client.add_handler(h)
    await asyncio.wait_for(client.check_role_change(), 5)
    assert h.add_working
    assert not h.remove_working

    client.web.get_json = AsyncMock(return_value=[])
    h.add_working = False
    await asyncio.wait_for(client.check_role_change(), 5)
    assert not h.add_working
    assert h.remove_working


@pytest.mark.asyncio
async def test_groupfeed_on_error(capsys, client: Phillip):
    client.web.get_users = AsyncMock(return_value=Exception)
    await client.check_role_change()
    _, err = capsys.readouterr()
    assert "error" in err


def test_disabled_check():
    with pytest.raises(Exception):
        Phillip("", disable_groupfeed=True, disable_mapfeed=True).start()
