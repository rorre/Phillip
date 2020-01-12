from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from phillip.helper import get_api, get_beatmap_api, get_discussion_json
from phillip.osu import Beatmap

class EventBase(ABC):
    """An Abstract Class (ABC) representing base osu! beatmapset event.
    """

    def __init__(self, soup: BeautifulSoup, nextevent: BeautifulSoup = None):
        self.soup = soup
        self.next_map = nextevent
        self._beatmapset = None
        self._beatmap = None

    async def get_beatmap(self):
        """Receive map from osu! API"""
        if not self._beatmap:
            map_id = self.soup.a.get("href").split("/")[4]
            self._beatmapset = await get_beatmap_api(s=map_id)
            self._beatmap = self.beatmapset[0]
        return self._beatmap

    @property
    def creator(self) -> str:
        """Mapper of beatmap."""
        return self.beatmap.creator

    @property
    def artist(self) -> str:
        """Beatmap's artist."""
        return self.beatmap.artist

    @property
    def title(self) -> str:
        """Beatmap's title."""
        return self.beatmap.title

    @property
    def map_cover(self) -> str:
        """URL to map's cover image."""
        return self.soup.a.img.get("src")

    @property
    def user_html(self):
        return self.soup.find(class_="beatmapset-event__content").a

    def user_action(self) -> str:
        """User in charge of the event."""
        return self.user_html.text.strip()

    def user_id_action(self) -> int:
        """``user_action``'s user id."""
        return int(self.user_html.get('data-user-id'))

    @property
    def time(self) -> datetime:
        """A ``datetime`` object representing the time where the event happened."""
        dt = self.soup.find(class_="timeago").get("datetime")
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S+00:00')

    @abstractmethod
    def event_type(self):
        """Event that happened on the beatmap (bubbled, qualified, etc.)"""
        pass

    @property
    def event_source_url(self) -> str:
        """URL to event cause."""
        return f"https://osu.ppy.sh/s/{self.beatmap.beatmapset_id}"

    @property
    def gamemodes(self) -> List[str]:
        """Game modes inside the beatmapset."""
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

    @property
    def source(self):
        """Representation of the beatmapset event source."""
        return Source(
            self.event_source_url,
            self.user_action(),
            self.user_id_action()
        )

    @property
    def beatmap(self) -> Beatmap:
        """First difficulty of the beatmap, usually the first entry from osu! API."""
        return self._beatmap

    @property
    def beatmapset(self) -> List[Beatmap]:
        """Array of difficulties inside the beatmap."""
        return self._beatmapset

class Source:
    """Representation of the beatmapset event source
    """

    def __init__(self, src_url: str, username: str = None, user_id: int = None,
                 post: dict = None, user: dict = None):
        self.src_url = src_url
        self._username = username
        self._user_id = user_id
        self._user = user
        self._post = post

    async def post(self) -> dict:
        """The post/thread causing the event. (raises ``Exception`` if its a Nomination post)
        """
        if "discussion" not in self.src_url:
            raise Exception("Nominations doesn't have posts.")
        if self._post:
            return self._post
        post_url = self.src_url
        post_id = int(post_url.split('/')[-1])
        discussion_parents = await get_discussion_json(post_url)
        sourcePost = None
        for discussion in discussion_parents:
            if not discussion:
                continue
            discussion_id = discussion.get("id")
            if discussion_id == post_id:
                sourcePost = discussion['posts'][0]
                break
        return sourcePost

    async def user(self) -> dict:
        """osu! API user object of the user that causes the event.
        """
        if self._user:
            return self._user
        api_response = list()
        if self._username:
            api_response = await get_api("get_user", u=self._username)
        elif self._user_id:
            api_response = await get_api("get_user", u=self._user_id)
        elif self.src_url:
            post = await self.post()
            api_response = await get_api("get_user", u=post['user_id'])
        return api_response[0]
