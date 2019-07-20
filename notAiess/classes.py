from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup

from . import helper

get_api = helper.get_api
get_beatmap_api = helper.get_beatmap_api
get_discussion_json = helper.get_discussion_json


class eventBase(ABC):
    """An Abstract Class (ABC) representing base osu! beatmapset event.

    Attributes
    ----------
    creator: str
        Mapper of beatmap.
    artist: str
        Beatmap's artist.
    title: str
        Beatmap's title.
    map_cover: str
        URL to map's cover image.
    user_action: str
        User in charge of the event.
    user_id_action: int
        ``user_action``'s user id.
    time: datetime
        A ``datetime`` object representing the time where the event happened.
    event_type: str
        Event that happened on the beatmap (bubbled, qualified, etc.)
    event_source_url: str
        URL to event cause.
    gamemodes: list of str
        Game modes inside the beatmapset.
    beatmap: osuClasses.Beatmap
        The difficulty of the beatmap, usually the first entry from osu! API. (Needs to run ``_get_map()``)
    beatmapset: list of osuClasses.Beatmap
        Array of difficulties inside the beatmap. (Needs to run ``_get_map()``)
    """

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    async def _get_map(self):
        """Receive map from osu! API and assign it to ``self.beatmapset`` and ``self.beatmap``"""
        map_id = self.soup.a.get("href").split("/")[4]
        self.beatmapset = await get_beatmap_api(s=map_id)
        self.beatmap = self.beatmapset[0]

    @property
    def creator(self) -> str:
        return self.beatmap.creator

    @property
    def artist(self) -> str:
        return self.beatmap.artist

    @property
    def title(self) -> str:
        return self.beatmap.title

    @property
    def map_cover(self) -> str:
        return self.soup.a.img.get("src")

    @property
    def user_action(self) -> str:
        return self.soup.find(class_="beatmapset-event__content").a.text.strip()

    @property
    def user_id_action(self) -> int:
        return int(self.soup.find(class_="beatmapset-event__content").a.get('data-user-id'))

    @property
    def time(self) -> datetime:
        dt = self.soup.find(class_="timeago").get("datetime")
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S+00:00')

    @property
    @abstractmethod
    def event_type(self):
        pass

    @property
    def event_source_url(self) -> str:
        return f"https://osu.ppy.sh/s/{self.beatmap.beatmapset_id}"

    @property
    def gamemodes(self) -> List[str]:
        mode_num = {
            "0": "osu",
            "1": "taiko",
            "2": "catch",
            "3": "mania"
        }
        modes = []
        for diff in self.beatmapset:
            if mode_num[diff.mode] not in modes:
                modes.append(mode_num[diff.mode])
        return modes


class Nominated(eventBase):
    @property
    def event_type(self) -> str:
        stat = str()
        if self.beatmap.approved == "3":
            stat = "Qualified"
        else:
            stat = "Bubbled"
        return stat


class Disqualified(eventBase):
    @property
    def event_type(self) -> str:
        return "Disqualified"

    @property
    def event_source_url(self) -> str:
        a_html = self.soup.find(
            class_="beatmapset-event__content").findAll("a")[1]
        post_url = a_html.get('href')
        return post_url

    @property
    def event_source(self) -> dict:
        post_url = self.event_source_url
        post_id = int(post_url.split('/')[-1])
        discussion_parents = await get_discussion_json(post_url)
        sourcePost = None
        for discussion in discussion_parents:
            if not discussion:
                continue
            if discussion['id'] == post_id:
                sourcePost = discussion['posts'][0]
                break
        return sourcePost


class Popped(Disqualified):
    @property
    def event_type(self) -> str:
        return "Popped"

    @property
    def event_source_url(self) -> str:
        a_html = self.soup.find(
            class_="beatmapset-event__content").findAll("a")[0]
        post_url = a_html.get('href')
        return post_url

    @property
    def event_source(self) -> dict:
        post_url = self.event_source_url
        post_id = int(post_url.split('/')[-1])
        discussion_parents = await get_discussion_json(post_url)
        sourcePost = None
        for discussion in discussion_parents:
            if not discussion:
                continue
            if discussion['id'] == post_id:
                sourcePost = discussion['posts'][0]
                break
        return sourcePost

    @property
    def user_id_action(self):
        return self.event_source['user_id']

    @property
    def user_action(self):
        return await get_api("get_user", u=self.user_id_action)[0]['username']


class Ranked(eventBase):
    @property
    def user_action(self):
        pass

    @property
    def user_id_action(self):
        pass

    @property
    def event_type(self):
        return "Ranked"


class Loved(Ranked):
    @property
    def event_type(self):
        return "Loved"
