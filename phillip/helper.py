from typing import List


def format_message(msg: str) -> str:
    message = msg.split("\n")[0]
    if len(message) < 20:
        message = msg[:80]
    if len(message) > 80:
        message = msg[:80] + "..."
    return message


async def gen_embed(event, app) -> dict:
    """Generate Aiess-styled Discord embed of event. 
    *This function is a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine).*

    **Parameters:**

    * event - `abc.EventBase` -- The beatmap's event.

    **Returns**

    * `dict` -- Discord embed object.
    """
    action_icons = {
        "Bubbled": ":thought_balloon:",
        "Qualified": ":heart:",
        "Ranked": ":sparkling_heart:",
        "Disqualified": ":broken_heart:",
        "Popped": ":anger_right:",
        "Loved": ":gift_heart:",
    }

    embed_base = {
        "title": f"{action_icons[event.event_type]} {event.event_type}",
        "description": f"[**{event.artist} - {event.title}**]({event.event_source_url})\r\n\
Mapped by {event.beatmap.creator} **[{']['.join(event.gamemodes)}]**",
        "color": 29625,
        "thumbnail": {"url": f"{event.map_cover}"},
    }

    if event.event_type not in ["Ranked", "Loved"]:
        apiuser = await event.source.user()
        user = apiuser["username"]
        user_id = apiuser["user_id"]
        embed_base["footer"] = {
            "icon_url": f"https://a.ppy.sh/{user_id}?1561560622.jpeg",
            "text": f"{user}",
        }

    if event.event_type in ["Popped", "Disqualified"]:
        source = await event.source.post()
        embed_base["footer"]["text"] += " - {}".format(
            format_message(source["message"])
        )
        embed_base["color"] = 15408128

    if event.event_type == "Ranked":
        users_str = str()
        history = await app.web.nomination_history(event.beatmap.beatmapset_id)
        for history_event in history:
            user = await app.api.get_api("get_user", u=history_event[1])
            u_name = user[0]["username"]

            if u_name == "BanchoBot":
                continue

            users_str += f"{action_icons[history_event[0]]} \
                [{u_name}](https://osu.ppy.sh/u/{history_event[1]}) "

        embed_base["description"] += "\r\n " + users_str

    return embed_base


def has_user(source: dict, target: List[dict]) -> bool:
    """Check if user is inside of another list

    **Parameters:**

    * source - `dict` -- User to be checked.
    * target - `List[dict]` -- List of users that will be compared to.

    **Returns**

    * `bool` -- Boolean value if user is inside another list or not.
    """
    if not target:
        return False

    for user in target:
        if source["id"] == user["id"]:
            return True
    return False
