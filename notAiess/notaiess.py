import asyncio
import signal
import sys
import traceback
from datetime import datetime, timedelta
from typing import List

import aiohttp
from pyee import AsyncIOEventEmitter

from . import helper
from .abc import Handler
from .event_helper import get_events


class SimpleHandler(Handler):
    async def on_map_event(self, event):
        """Parse beatmap event and send to discord webhook |coro|

        Parameters
        ----------
        event: [:class:`EventBase`]
            The beatmapset event
        """
        embed = await helper.gen_embed(event)
        with aiohttp.ClientSession() as session:
            await session.post(self.hook_url, json={
                'content': event.event_source_url,
                'embeds': [embed]
            })
        return


class notAiess:
    """Representation of Aiess client to interact with osu! web.
    This client will interact with osu! API and web through scraper.

    Parameters
    ----------
    token: str
        osu! API token, could be gathered `here <https://osu.ppy.sh/p/api>`_
    last_date: datetime, optional
        Custom checkpoint to check every event after last_date, defaults to None
    handlers: list of Handler, optional
        Event handlers assigned to be called, defaults to [Handler]
    webhook_url: str, optional
        **Discord** webhook url if there is no handlers assigned, defaults to empty string

    Raises
    ------
    Exception
        if no handlers nor webhook_url assigned.
    """

    def __init__(self, token: str, last_date: datetime = None, handlers: List[Handler] = None,
                 webhook_url: str = "", loop=None, emitter: AsyncIOEventEmitter = None):
        if not handlers:
            self.handlers = []
        else:
            self.handlers = handlers
        self.webhook_url = webhook_url
        self.apitoken = token
        helper.APIKEY = token
        self.last_date = last_date or datetime.utcfromtimestamp(0)
        self.loop = loop or asyncio.get_event_loop()
        self.last_event = None
        self.closed = False
        self.group_ids = [
            # https://github.com/ppy/osu-web/blob/master/app/Models/UserGroup.php
            4,  # GMT
            7,  # NAT
            16,  # Alumni
            28,  # Full BN
            32  # Probation BN
        ]
        self.last_users = dict()
        for gid in self.group_ids:
            self.last_users[gid] = list()

        self.emitter = emitter or AsyncIOEventEmitter()

        for handler in handlers:
            handler.register_emitter(self.emitter)

    async def check_map_events(self):
        """Check for map events. |coro|
        """
        events = [event async for event in get_events((1, 1, 1, 1, 1))]
        for i, event in enumerate(events):
            if event.time >= self.last_date:
                await event._get_map()

                if event.time == self.last_date:
                    if self.last_event:
                        if not self.last_event.beatmapset:
                            await self.last_event.beatmapset
                        if event.beatmapset[0].beatmapset_id == self.last_event.beatmapset[0].beatmapset_id:
                            continue

                if event.time == self.last_date and i + 1 == len(events):
                    self.last_date = event.time + timedelta(seconds=1)
                else:
                    self.last_date = event.time

                self.last_event = event
                if event.event_type not in ["Ranked", "Loved"]:
                    user = await event.source.user()
                    if user['username'] == "BanchoBot":
                        continue

                self.emitter.emit("map_event", event)
                self.emitter.emit(event.event_type.lower(), event)

    async def check_role_change(self):
        """Check for role changes. |coro|
        """
        for gid in self.group_ids:
            users = await helper.get_users(gid)

            for user in users:
                if not helper.has_user(user, self.last_users[gid]):
                    self.emitter.emit("group_add", user)
                    self.emitter.emit(user.default_group, user)

            for user in self.last_users[gid]:
                if not helper.has_user(user, users):
                    self.emitter.emit("group_removed", user)
                    self.emitter.emit(user.default_group, user)

            self.last_users[gid] = users

    async def start(self):
        """Well, run the client, what else?! |coro|"""
        if not self.handlers:
            if not self.webhook_url:
                raise Exception("Requires Handler or webhook_url")
            self.handlers.append(Handler(self.webhook_url))

        while not self.closed:
            try:
                event = asyncio.create_task(self.check_map_events())
                role = asyncio.create_task(self.check_role_change())

                await event
                await role
                await asyncio.sleep(300)

            except:
                print("An error occured, will keep running anyway.", file=sys.stderr)
                traceback.print_exc()

    def add_handler(self, handler):
        """Adds custom handler to handlers.

        Parameters
        ----------
        handler: object
            The event handler, class must have `parse` function with `event` as argument.
        """
        self.handlers.append(handler)

    def run(self):
        """Run notAiess. This function does not take any parameter.
        """
        def stop():
            self.closed = True
            self.loop.stop()

        try:
            self.loop.add_signal_handler(signal.SIGINT, stop)
            self.loop.add_signal_handler(signal.SIGTERM, stop)
        except NotImplementedError:
            pass

        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            stop()
            self.loop.close()
