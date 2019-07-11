import sys
import time
from datetime import datetime
from typing import List

import requests

from . import helper
from . import event_helper

get_events = event_helper.get_events


class Handler:
    def __init__(self, webhook_url):
        self.hook_url = webhook_url

    def parse(self, event):
        embed = helper.gen_embed(event)
        requests.post(self.hook_url, json={
            'content': event.event_source_url,
            'embeds': [embed]
        })
        return


class notAiess:
    def __init__(self, token: str, last_date: datetime = None, handlers: List[Handler] = [],
                 webhook_url: str = ""):
        self.handlers = handlers
        if not handlers:
            if not webhook_url:
                raise Exception("Requires Handler or webhook_url")
            self.handlers.append(Handler(webhook_url))
        self.apitoken = token
        helper.apikey = token
        self.last_date = last_date or datetime.utcfromtimestamp(0)

    def run(self):
        try:
            while True:
                events = get_events((1, 1, 1, 1, 1))
                events.reverse()
                for event in events:
                    if event.time > self.last_date:
                        self.last_date = event.time
                        if event.user_action == "BanchoBot":
                            continue
                        for handler in self.handlers:
                            handler.parse(event)

                time.sleep(300)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)

        except:
            self.run()  # Forever loop

    def add_handler(self, handler):
        self.handlers.append(handler)
