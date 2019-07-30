import sys
import time
import asyncio
from datetime import datetime
from typing import List
import traceback
import requests_async as requests
import signal

from . import helper
from . import event_helper

get_events = event_helper.get_events


class Handler:
    """Handler base for ``notAiess``

    Parameters
    ----------
    webhook_url: str
        Discord webhook url to send
    """

    def __init__(self, webhook_url):
        self.hook_url = webhook_url

    async def parse(self, event):
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

    def __init__(self, token: str, last_date: datetime = None, handlers: List[Handler] = [],
                 webhook_url: str = "", loop = None):
        self.handlers = handlers
        self.webhook_url = webhook_url
        self.apitoken = token
        helper.apikey = token
        self.last_date = last_date or datetime.utcfromtimestamp(0)
        self.loop = None
        self.last_event = None

    async def start(self):
        """Well, run the client, what else?! |coro|"""
        if not self.handlers:
            if not self.webhook_url:
                raise Exception("Requires Handler or webhook_url")
            self.handlers.append(Handler(self.webhook_url))

        while True:
            try:
                async for event in get_events((1, 1, 1, 1, 1)):
                    if event.time >= self.last_date and self.last_event != event:
                        self.last_date = event.time
                        await event._get_map()
                        if event.event_type not in ["Ranked", "Loved"]:
                            user = await event.source.user
                            if user['username'] == "BanchoBot":
                                continue
                        for handler in self.handlers:
                            await handler.parse(event)
                        self.last_event = event

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
        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.start())

        try:
            self.loop.add_signal_handler(signal.SIGINT, lambda: self.loop.stop())
            self.loop.add_signal_handler(signal.SIGTERM, lambda: self.loop.stop())
        except NotImplementedError:
            pass

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()
