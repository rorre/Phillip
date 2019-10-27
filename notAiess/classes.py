from .abc import EventBase, Source
from .helper import get_api, get_discussion_json


class Nominated(EventBase):
    @property
    def event_type(self) -> str:
        stat = "Bubbled"
        if self.next_map:
            map_content = self.next_map.find(class_="beatmapset-event__content")
            action = map_content.text.strip().split()[0]
            if action == "This":
                stat = "Qualified"
        return stat


class Disqualified(EventBase):
    @property
    def event_type(self) -> str:
        return "Disqualified"

    @property
    def event_source_url(self) -> str:
        a_html = self.soup.find(
            class_="beatmapset-event__content").findAll("a")[1]
        post_url = a_html.get('href')
        return post_url


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

    async def event_source(self) -> dict:
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

    async def user_id_action(self):
        source = await self.event_source()
        return source['user_id']

    async def user_action(self):
        user_source_id = await self.user_id_action()
        api_response = await get_api("get_user", u=user_source_id)
        return api_response[0]['username']

    @property
    def source(self):
        return Source(self.event_source_url)


class Ranked(EventBase):
    def user_action(self):
        pass

    def user_id_action(self):
        pass

    @property
    def event_type(self):
        return "Ranked"


class Loved(Ranked):
    @property
    def event_type(self):
        return "Loved"
