from phillip.abc import EventBase


class Nominated(EventBase):
    @property
    def event_type(self) -> str:
        stat = "Bubbled"
        if self.next_event and self.next_event["type"] == "qualify":
            stat = "Qualified"
        return stat


class Disqualified(EventBase):
    @property
    def event_type(self) -> str:
        return "Disqualified"

    @property
    def event_source_url(self) -> str:
        discussion_id = self.js["comment"]["beatmap_discussion_id"]
        return f"https://osu.ppy.sh/beatmapsets/beatmap-discussions/{discussion_id}"


class Popped(Disqualified):
    @property
    def event_type(self) -> str:
        return "Popped"


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
