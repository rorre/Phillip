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
        self._register_events()

    def _register_events(self):
        for func in dir(self):
            if not func.startswith("on_"): continue
            if func == "on_map_event":
                emitter.on("map_event", getattr(self, func))
            elif func == "on_group_added":
                emitter.on("group_added", getattr(self, func))
            elif func == "on_group_removed":
                emitter.on("group_removed", getattr(self, func))
            elif func == "on_group_probation":
                emitter.on("bng_limited", getattr(self, func))
            else:
                emitter.on(func.split("_")[-1], getattr(self, func))

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
    
    async def on_map_bubbled(self, event):
        pass

    async def on_map_qualified(self, event):
        pass

    async def on_map_disqualified(self, event):
        pass

    async def on_map_popped(self, event):
        pass

    async def on_map_ranked(self, event):
        pass

    async def on_map_loved(self, event):
        pass

    async def on_group_added(self, user):
        pass

    async def on_group_removed(self, user):
        pass

    async def on_group_probation(self, user):
        pass
    
    async def on_group_gmt(self, user):
        pass

    async def on_group_bng(self, user):
        pass
    
    async def on_group_nat(self, user):
        pass

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

                emitter.emit("map_event", event)
                emitter.emit(event.event_type.lower(), event)

    async def check_role_change(self):
        for gid in self.group_ids:
            users = await helper.get_users(gid)

            for user in users:
                if not helper.has_user(user, self.last_users[gid]):
                    emitter.emit("group_add", user)
                    emitter.emit(user['default_group'], user)
            
            for user in self.last_users[gid]:
                if not helper.has_user(user, users):
                    emitter.emit("group_removed", user)
                    emitter.emit(user['default_group'], user)

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

            except KeyboardInterrupt as e:
                raise e

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
