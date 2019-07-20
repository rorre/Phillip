import json
from typing import List

import requests_async as requests
from bs4 import BeautifulSoup

from . import osuClasses

Beatmap = osuClasses.Beatmap

base_api_url = "https://osu.ppy.sh/api/"
apikey = None


async def get_api(endpoint: str, **kwargs: dict) -> List[dict]:
    """Request something based on endpoint.

    Parameters
    ----------
    endpoint: str
        The API endpoint, reference could be found `here <https://github.com/ppy/osu-api/wiki>`_.
    **kwargs: dict, optional
        Keyword arguments that will be passed as a query string.

    Raises
    ------
        Exception
            If the API key is not assigned.

    Returns
    -------
    List[dict]
        API response.
    """

    global apikey
    if not apikey:
        raise Exception("Requires api key to be set")
    kwargs['k'] = apikey
    api_arguments = list()
    for argument in kwargs.items():
        api_arguments.append(f"{argument[0]}={str(argument[1])}")
    api_args = '&'.join(api_arguments)
    api_url = base_api_url + endpoint + "?" + api_args
    api_res = await requests.get(api_url)
    return api_res.json()


async def get_beatmap_api(**kwargs: dict) -> List[Beatmap]:
    """Get beatmapset from osu! API.

    Returns
    -------
    List[Beatmap]
        Beatmapsets fetched from API.
    """
    return [Beatmap(map) for map in await get_api("get_beatmaps", **kwargs)]


async def get_discussion_json(uri: str) -> List[dict]:
    """Receive discussion posts in JSON.

    Parameters
    ----------
    uri: str
        URL of discussion page.

    Returns
    -------
    List[dict]
        The discussion posts.
    """

    set_html = await requests.get(uri).text
    soup = BeautifulSoup(set_html, features="html.parser")
    set_json_str = soup.find(id="json-beatmapset-discussion").text
    set_json = json.loads(set_json_str)
    return set_json['beatmapset']['discussions']


def gen_embed(event) -> dict:
    """Generate Discord embed of event.

    Parameters
    ----------
    event: eventBase
        The beatmap's event.

    Returns
    -------
    dict
        Discord embed object.
    """

    action_icons = {
        "Bubbled": ":thought_balloon:",
        "Qualified": ":heart:",
        "Ranked": ":sparkling_heart:",
        "Disqualified": ":broken_heart:",
        "Popped": ":anger_right:",
        "Loved": ":gift_heart:"
    }
    embed_base = {
        "title": f"{action_icons[event.event_type]} {event.event_type}",
        "description": f"[**{event.artist} - {event.title}**]({event.event_source_url})\r\n\
Mapped by {event.beatmap.creator} **[{']['.join(event.gamemodes)}]**",
        "color": 29625,
        "thumbnail": {
            "url": f"{event.map_cover}"
        }
    }
    if event.event_type not in ["Ranked", "Loved"]:
        embed_base['footer'] = {
            "icon_url": f"https://a.ppy.sh/{event.user_id_action}?1561560622.jpeg",
            "text": f"{event.user_action}"
        }
    if event.event_type in ["Popped", "Disqualified"]:
        embed_base['footer']['text'] += " - {}".format(
            event.event_source['message'].split("\n")[0])
        embed_base['color'] = 15408128
    return embed_base


def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
