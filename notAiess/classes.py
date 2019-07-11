from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from . import helper

get_api = helper.get_api
get_beatmap_api = helper.get_beatmap_api
get_discussion_json = helper.get_discussion_json

class eventBase(ABC):
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self._get_map()

    def _get_map(self):
        map_id = self.soup.a.get("href").split("/")[4]
        self.beatmap = get_beatmap_api(s=map_id)[0]

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


class Nominated(eventBase):
    @property
    def event_type(self) -> str:
        return "Nominated"


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
        discussion_parents = get_discussion_json(post_url)
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
        discussion_parents = get_discussion_json(post_url)
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
        return get_api("get_user", u=self.user_id_action)[0]['username']

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