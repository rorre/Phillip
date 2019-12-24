from typing import Generator, List

import aiohttp
from bs4 import BeautifulSoup

from . import abc, classes
from .helper import throttler

BASE_URL = "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D="

TYPES = [
    "nominate",
    "rank",
    "love",
    "nomination_reset",
    "disqualify"
]


async def get_events(types_val: list) -> Generator[List[abc.EventBase], None, None]:
    """Get events of from osu!website. |coro|

    Parameters
    ----------
    types_val : list
        A list consisting of 5 integer, with value of either 0 or 1 for the value of [nominate, rank, love, nomination_reset, disqualify]
]

    Yields
    -------
    list of abc.EventBase
        List of events resulted from fetching osu!web, with next index as next event that will be processed.
    """
    additions = list()
    async with throttler:
        async with aiohttp.ClientSession() as session:
            for i in range(5):
                additions.append(types_val[i] and TYPES[i] or str())
            if types_val[0]:
                additions.append("qualify")
            url = BASE_URL + '&types%5B%5D='.join(additions)

            async with session.get(url, cookies={"locale": "en"}) as res:
                res_soup = BeautifulSoup(await res.text(), features="html.parser")

    events_html = res_soup.findAll(class_="beatmapset-event")
    events_html.reverse()

    event_cases = {
        "Nominated": classes.Nominated,
        "Disqualified": classes.Disqualified,
        "New": classes.Popped,
        "Ranked.": classes.Ranked,
        "Loved": classes.Loved
    }

    for i, event in enumerate(events_html):
        action = event.find(
            class_="beatmapset-event__content").text.strip().split()[0]

        if action == "This":
            continue  # Skip qualified event news

        next_map = None
        if i + 1 != len(events_html):
            next_map = events_html[i+1]

        yield event_cases[action](event, next_map)
