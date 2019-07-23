import requests_async as requests
from bs4 import BeautifulSoup

from . import classes

base_url = "https://osu.ppy.sh/beatmapsets/events?user=&types%5B%5D="

types = [
    "nominate",
    "rank",
    "love",
    "nomination_reset",
    "disqualify"
]


async def get_events(types_val: list) -> str:
    additions = list()
    for i in range(5):
        additions.append(types_val[i] and types[i] or str())
    url = base_url + '&types%5B%5D='.join(additions)
    res = await requests.get(url, cookies={"locale": "en"})
    res_soup = BeautifulSoup(res.text, features="html.parser")
    events_html = res_soup.findAll(class_="beatmapset-event")
    events_html.reverse()
    events = []
    event_cases = {
        "Nominated": classes.Nominated,
        "Disqualified": classes.Disqualified,
        "New": classes.Popped,
        "Ranked.": classes.Ranked,
        "Loved": classes.Loved
    }
    for event in events_html:
        action = event.find(
            class_="beatmapset-event__content").text.strip().split()[0]
        yield event_cases[action](event)
