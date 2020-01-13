
class Beatmap:
    """A class that represents a difficulty object inside a beatmapset

    Parameters
    ----------
    js: dict
        osu! API response, gathered from ``get_beatmaps`` endpoint

    Attributes
    ----------
    All: str
        Everything that is documented from `osu! API wiki <https://github.com/ppy/osu-api/wiki>`_.
    """

    def __init__(self, js):
        self.beatmapset_id = js['beatmapset_id']
        self.beatmap_id = js['beatmap_id']
        self.approved = js['approved']
        self.total_length = js['total_length']
        self.hit_length = js['hit_length']
        self.version = js['version']
        self.file_md5 = js['file_md5']
        self.diff_size = js['diff_size']
        self.diff_overall = js['diff_overall']
        self.diff_approach = js['diff_approach']
        self.diff_drain = js['diff_drain']
        self.mode = js['mode']
        self.count_normal = js['count_normal']
        self.count_slider = js['count_slider']
        self.count_spinner = js['count_spinner']
        self.submit_date = js['submit_date']
        self.approved_date = js['approved_date']
        self.last_update = js['last_update']
        self.artist = js['artist']
        self.title = js['title']
        self.creator = js['creator']
        self.creator_id = js['creator_id']
        self.bpm = js['bpm']
        self.source = js['source']
        self.tags = js['tags']
        self.genre_id = js['genre_id']
        self.language_id = js['language_id']
        self.favourite_count = js['favourite_count']
        self.rating = js['rating']
        self.download_unavailable = js['download_unavailable']
        self.audio_unavailable = js['audio_unavailable']
        self.playcount = js['playcount']
        self.passcount = js['passcount']
        self.max_combo = js['max_combo']
        self.diff_aim = js['diff_aim']
        self.diff_speed = js['diff_speed']
        self.difficultyrating = js['difficultyrating']

class GroupUser:
    """A class representing a user inside a grup.

    Parameters
    ----------
    obj: dict
        osu! json object, gathered from groups page.

    Attributes
    ----------
    id: int
        osu! user ID.
    username : str
        osu! username.
    profile_colou : str
        Hex of user's role color.
    avatar_url: str
        User's avatar URL.
    country_code: str
        Country code of user.
    default_group: str
        Highest group of the user.
    is_active: bool
        Representation if user is still active on osu! or not.
    is_bot: bool
        Is user a bot?
    is_online: bool
        Is the user is only at the moment or not.
    is_supporter: bool
        Does the user have supporter tag?
    last_visit: str
        User's last login to osu!
    pm_friends_only: bool
        Represents if user only enables forum pm to friends only or not.
    country: dict
        A dictionary with key of code and name, representing the country code and full country name respectively.
    cover: dict
        A dictionary with custom_url, id, and url as key, representing cover url, id, and cover url respectively.
    support_level: int
        Supporter tag level of user.
    """
    def __init__(self, obj):
        self.id = obj['id']
        self.username = obj['username']
        self.profile_colour = obj['profile_colour']
        self.avatar_url = obj['avatar_url']
        self.country_code = obj['country_code']
        self.default_group = obj['default_group']
        self.is_active = obj['is_active']
        self.is_bot = obj['is_bot']
        self.is_online = obj['is_online']
        self.is_supporter = obj['is_supporter']
        self.last_visit = obj['last_visit']
        self.pm_friends_only = obj['pm_friends_only']
        self.country = obj['country']
        self.cover = obj['cover']
        self.support_level = obj['support_level']
