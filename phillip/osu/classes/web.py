class Beatmap:
    def __init__(self, js):
        self.artist = js.get("artist")
        self.covers = js.get("covers")
        self.creator = js.get("creator")
        self.favourite_count = js.get("favourite_count")
        self.id = js.get("id")
        self.play_count = js.get("play_count")
        self.preview_url = js.get("preview_url")
        self.source = js.get("source")
        self.status = js.get("status")
        self.title = js.get("title")
        self.user_id = js.get("user_id")
        self.video = js.get("video")
        self.user = User(js.get("user"))


class User:
    def __init__(self, js):
        self.avatar_url = js.get("avatar_url")
        self.country_code = js.get("country_code")
        self.default_group = js.get("default_group")
        self.id = js.get("id")
        self.is_active = js.get("is_active")
        self.is_bot = js.get("is_bot")
        self.is_online = js.get("is_online")
        self.is_supporter = js.get("is_supporter")
        self.last_visit = js.get("last_visit")
        self.pm_friends_only = js.get("pm_friends_only")
        self.profile_colour = js.get("profile_colour")
        self.username = js.get("username")


class Discussion:
    def __init__(self, js):
        self.id = js.get("id")
        self.beatmapset_id = js.get("beatmapset_id")
        self.beatmap_id = js.get("beatmap_id")
        self.user_id = js.get("user_id")
        self.deleted_by_id = js.get("deleted_by_id")
        self.message_type = js.get("message_type")
        self.parent_id = js.get("parent_id")
        self.timestamp = js.get("timestamp")
        self.resolved = js.get("resolved")
        self.can_be_resolved = js.get("can_be_resolved")
        self.can_grant_kudosu = js.get("can_grant_kudosu")
        self.created_at = js.get("created_at")
        self.updated_at = js.get("updated_at")
        self.deleted_at = js.get("deleted_at")
        self.last_post_at = js.get("last_post_at")
        self.kudosu_denied = js.get("kudosu_denied")
        self.starting_post = Post(js.get("starting_post"))


class Post:
    def __init__(self, js):
        self.id = js.get("id")
        self.beatmap_discussion_id = js.get("beatmap_discussion_id")
        self.user_id = js.get("user_id")
        self.last_editor_id = js.get("last_editor_id")
        self.deleted_by_id = js.get("deleted_by_id")
        self.system = js.get("system")
        self.message = js.get("message")
        self.created_at = js.get("created_at")
        self.updated_at = js.get("updated_at")
        self.deleted_at = js.get("deleted_at")


class GroupUser:
    """A class representing a user inside a grup.

    **Parameters:**

    * obj - `dict` -- osu! json object, gathered from groups page.

    **Attributes:**

    * id - `int` -- osu! user ID.
    * username - `str` -- osu! username.
    * profile_colour - `str` -- Hex of user's role color.
    * avatar_url - `str` -- User's avatar URL.
    * country_code - `str` -- Country code of user.
    * default_group - `str` -- Highest group of the user.
    * is_active - `bool` -- Representation if user is still active on osu! or not.
    * is_bot - `bool` -- Is user a bot?
    * is_online - `bool` -- Is the user is only at the moment or not.
    * is_supporter - `bool` -- Does the user have supporter tag?
    * last_visit - `str` -- User's last login to osu!
    * pm_friends_only - `bool` -- Represents if user only enables forum pm to friends only or not.
    * country - `dict` -- A dictionary with key of code and name, representing the country code and full country name respectively.
    * cover - `dict` -- A dictionary with custom_url, id, and url as key, representing cover url, id, and cover url respectively.
    * support_level - `int` -- Supporter tag level of user.
    """

    def __init__(self, obj):
        self.id = obj["id"]
        self.username = obj["username"]
        self.profile_colour = obj["profile_colour"]
        self.avatar_url = obj["avatar_url"]
        self.country_code = obj["country_code"]
        self.default_group = obj["default_group"]
        self.is_active = obj["is_active"]
        self.is_bot = obj["is_bot"]
        self.is_online = obj["is_online"]
        self.is_supporter = obj["is_supporter"]
        self.last_visit = obj["last_visit"]
        self.pm_friends_only = obj["pm_friends_only"]
        self.country = obj["country"]
        self.cover = obj["cover"]
        self.support_level = obj["support_level"]
