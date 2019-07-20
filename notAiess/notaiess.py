import sys
import time
from datetime import datetime
from typing import List
import traceback
import requests

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

    def parse(self, event):
        """Parse beatmap event and send to discord webhook

        Parameters
        ----------
        event: [:class:`eventBase`]
            The beatmapset event
        """
        embed = helper.gen_embed(event)
        requests.post(self.hook_url, json={
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
                 webhook_url: str = ""):
        self.handlers = handlers
        self.webhook_url = webhook_url
        self.apitoken = token
        helper.apikey = token
        self.last_date = last_date or datetime.utcfromtimestamp(0)

    def run(self):
        """Well, run the client, what else?!"""
        if not self.handlers:
            if not self.webhook_url:
                raise Exception("Requires Handler or webhook_url")
            self.handlers.append(Handler(self.webhook_url))
        try:
            while True:
                events = get_events((1, 1, 1, 1, 1))
                events.reverse()
                for event in events:
                    if event.time > self.last_date:
                        self.last_date = event.time
                        event._get_map()
                        if event.user_action == "BanchoBot":
                            continue
                        for handler in self.handlers:
                            handler.parse(event)

                time.sleep(300)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

        except:
            print("An error occured, will keep running anyway.")
            traceback.print_exc()
            self.run()  # Forever loop

    def add_handler(self, handler):
        """Adds custom handler to handlers.

        Parameters
        ----------
        handler: object
            The event handler, class must have `parse` function with `event` as argument.
        """
        self.handlers.append(handler)
