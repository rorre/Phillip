import json
from typing import List, Tuple

import requests_async as requests
from bs4 import BeautifulSoup
from . import osuClasses

Beatmap = osuClasses.Beatmap

BASE_API_URL = "https://osu.ppy.sh/api/"
BASE_GROUPS_URL = "https://osu.ppy.sh/groups/"
APIKEY = None

EVENTS = {
    "nominate": "Bubbled",
    "disqualify": "Disqualified",
    "nomination_reset": "Popped",
}

async def get_api(endpoint: str, **kwargs: dict) -> List[dict]:
    """Request something based on endpoint. |coro|

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

    global APIKEY
    if not APIKEY:
        raise Exception("Requires api key to be set")
    kwargs['k'] = APIKEY
    api_arguments = list()
    for argument in kwargs.items():
        api_arguments.append(f"{argument[0]}={str(argument[1])}")
    api_args = '&'.join(api_arguments)
    api_url = BASE_API_URL + endpoint + "?" + api_args
    api_res = await requests.get(api_url)
    return api_res.json()


async def get_beatmap_api(**kwargs: dict) -> List[Beatmap]:
    """Get beatmapset from osu! API. |coro|

    Returns
    -------
    List[Beatmap]
        Beatmapsets fetched from API.
    """
    return [Beatmap(map) for map in await get_api("get_beatmaps", **kwargs)]


async def get_discussion_json(uri: str) -> List[dict]:
    """Receive discussion posts in JSON. |coro|

    Parameters
    ----------
    uri: str
        URL of discussion page.

    Returns
    -------
    List[dict]
        The discussion posts.
    """

    set_html = await requests.get(uri)
    soup = BeautifulSoup(set_html.text, features="html.parser")
    set_json_str = soup.find(id="json-beatmapset-discussion").text
    set_json = json.loads(set_json_str)
    return set_json['beatmapset']['discussions']


async def gen_embed(event) -> dict:
    """Generate Discord embed of event. |coro|

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
        apiuser = await event.source.user()
        user = apiuser['username']
        user_id = apiuser['user_id']
        embed_base['footer'] = {
            "icon_url": f"https://a.ppy.sh/{user_id}?1561560622.jpeg",
            "text": f"{user}"
        }
    if event.event_type in ["Popped", "Disqualified"]:
        source = await event.source.post()
        embed_base['footer']['text'] += " - {}".format(
            source['message'].split("\n")[0])
        embed_base['color'] = 15408128
    if event.event_type == "Ranked":
        s = str()
        history = await nomination_history(event.beatmap.beatmapset_id)
        for h in history:
            u = await get_api("get_user", u=h[1])
            usern = u[0]['username']
            if usern == "BanchoBot": continue
            s += f"{action_icons[h[0]]} [{usern}](https://osu.ppy.sh/u/{h[1]}) "
        embed_base['description'] += "\r\n " + s
    return embed_base


async def nomination_history(mapid: int) -> List[Tuple[str, int]]:
    """Get nomination history of a beatmap.
    
    Parameters
    ----------
    mapid : int
        Beatmapset ID that will be gathered.
    
    Returns
    -------
    List[Tuple[str, int]]
        A list containing tuple with a string with event type and user id of user triggering the event.
    """
    discussion_url = f"https://osu.ppy.sh/beatmapsets/{str(mapid)}/discussion"
    set_html = await requests.get(discussion_url)
    soup = BeautifulSoup(set_html.text, features="html.parser")
    set_json_str = soup.find(id="json-beatmapset-discussion").text
    set_json = json.loads(set_json_str)
    js = set_json['beatmapset']['events']
    history = []
    for i, event in enumerate(js):
        if i + 1 != len(js):
            next_event = js[i+1]
        if event['type'] in EVENTS:
            e = EVENTS[event['type']]
            if next_event['type'] == "qualify":
                e = "Qualified"
            history.append((e, event['user_id']))
    return history

async def get_users(group_id: int) -> List[dict]:
    """Get users inside of a group
    
    Parameters
    ----------
    group_id : int
        The group id.
    
    Returns
    -------
    List[dict]
        A dictionary containing users' data.
    """
    r = await requests.get(BASE_GROUPS_URL + str(group_id))
    res = r.text
    bs = BeautifulSoup(res, features="html.parser")
    users_tag = bs.find(id="json-users").text
    users_json = json.loads(users_tag)
    return users_json

def has_user(source: dict, target: List[dict]) -> bool:
    """Check if user is inside of another list
    
    Parameters
    ----------
    source : dict
        User to be checked.
    target : List[dict]
        List of users that will be compared to.
    
    Returns
    -------
    bool
        Boolean value if user is inside another list or not.
    """
    if not target:
        return False

    for user in target:
        if source['id'] == user['id']:
            return True
    return False