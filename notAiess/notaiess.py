import sys
import time
from datetime import datetime

import requests

from . import helper
from . import event_helper

get_events = event_helper.get_events


class notAiess:
    def __init__(self, token: str, webhook_url: str, last_date: datetime = None):
        self.apitoken = token
        helper.apikey = token
        self.hook_url = webhook_url
        self.last_date = last_date or datetime.utcfromtimestamp(0)

    def run(self):
        try:
            while True:
                events = get_events((1, 0, 0, 0, 1, 1))
                events.reverse()
                embeds = []
                for event in events:
                    if event.time > self.last_date:
                        self.last_date = event.time
                        if event.user_action == "BanchoBot":
                            continue
                        embed = helper.gen_embed(event)
                        embeds.append(embed)

                for e in helper.chunk(embeds, 10):
                    requests.post(self.hook_url, json={'embeds': e})
                time.sleep(300)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)
