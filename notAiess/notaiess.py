import asyncio
import signal
import sys
import traceback
from datetime import datetime, timedelta
from typing import List

import requests_async as requests
from pyee import AsyncIOEventEmitter

from . import helper
from .event_helper import get_events

emitter = AsyncIOEventEmitter()


class Handler:
    """Handler base for ``notAiess``

    Parameters
    ----------
    webhook_url: str
        Discord webhook url to send
    """
    

    def __init__(self, webhook_url):
        self.hook_url = webhook_url

    @emitter.on('map_event')
    async def on_map_event(self, event):
        """Parse beatmap event and send to discord webhook |coro|

        Parameters
        ----------
        event: [:class:`eventBase`]
            The beatmapset event
        """
        embed = await helper.gen_embed(event)
        await requests.post(self.hook_url, json={
            'content': event.event_source_url,
            'embeds': [embed]
        })
        return
    
    @emitter.on('Bubbled')
    async def on_map_bubbled(self, event):
        pass

    @emitter.on('Qualified')
    async def on_map_qualified(self, event):
        pass

    @emitter.on('Disqualified')
    async def on_map_disqualified(self, event):
        pass

    @emitter.on('Popped')
    async def on_map_popped(self, event):
        pass

    @emitter.on('Ranked')
    async def on_map_ranked(self, event):
        pass

    @emitter.on('Loved')
    async def on_map_loved(self, event):
        pass

    @emitter.on('group_added')
    async def on_group_added(self, user):
        pass

    @emitter.on('group_removed')
    async def on_group_removed(self, user):
        pass

    @emitter.on('bng_limited')
    async def on_group_probation(self, user):
        pass
    
    @emitter.on('gmt')
    async def on_group_gmt(self, user):
        pass

    @emitter.on('bng')
    async def on_group_bng(self, user):
        pass
    
    @emitter.on('nat')
    async def on_group_nat(self, user):
        pass

    @emitter.on('alumni')
    async def on_group_alumni(self, user):
        pass

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

    def __init__(self, token: str, last_date: datetime = None, handlers: List[Handler] = list(),
                 webhook_url: str = "", loop=None):
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
            16, # Alumni
            28, # Full BN
            32  # Probation BN
        ]
        self.last_users = dict()
        for gid in self.group_ids:
            self.last_users[gid] = list()

    async def check_map_events(self):
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

                for handler in self.handlers:
                    emitter.emit("map_event", handler, event)
                    emitter.emit(event.event_type, handler, event)

    async def check_role_change(self):
        for gid in self.group_ids:
            users = await helper.get_users(gid)

            for user in users:
                if not helper.has_user(user, self.last_users[gid]):
                    for handler in self.handlers:
                        emitter.emit("group_add", handler, user)
                        emitter.emit(user['default_group'], handler, user)
            
            for user in self.last_users[gid]:
                if not helper.has_user(user, users):
                    for handler in self.handlers:
                        emitter.emit("group_removed", handler, user)
                        emitter.emit(user['default_group'], handler, user)

            self.last_users[gid] = users

    async def start(self):
        """Well, run the client, what else?! |coro|"""
        if not self.handlers:
            if not self.webhook_url:
                raise Exception("Requires Handler or webhook_url")
            self.handlers.append(Handler(self.webhook_url))

        while not self.closed:
            try:
                await self.check_map_events()
                await self.check_role_change()
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
