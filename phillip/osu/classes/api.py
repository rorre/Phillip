class Beatmap:
    """A class that represents a difficulty object inside a beatmapset

    **Parameters:**

    * js - `dict` -- osu! API response, gathered from ``get_beatmaps`` endpoint

    **Attributes:**

    * All - `str` -- Everything that is documented from [osu! API wiki](https://github.com/ppy/osu-api/wiki).
    """

    def __init__(self, js):
        self.beatmapset_id = js["beatmapset_id"]
        self.beatmap_id = js["beatmap_id"]
        self.approved = js["approved"]
        self.total_length = js["total_length"]
        self.hit_length = js["hit_length"]
        self.version = js["version"]
        self.file_md5 = js["file_md5"]
        self.diff_size = js["diff_size"]
        self.diff_overall = js["diff_overall"]
        self.diff_approach = js["diff_approach"]
        self.diff_drain = js["diff_drain"]
        self.mode = js["mode"]
        self.count_normal = js["count_normal"]
        self.count_slider = js["count_slider"]
        self.count_spinner = js["count_spinner"]
        self.submit_date = js["submit_date"]
        self.approved_date = js["approved_date"]
        self.last_update = js["last_update"]
        self.artist = js["artist"]
        self.title = js["title"]
        self.creator = js["creator"]
        self.creator_id = js["creator_id"]
        self.bpm = js["bpm"]
        self.source = js["source"]
        self.tags = js["tags"]
        self.genre_id = js["genre_id"]
        self.language_id = js["language_id"]
        self.favourite_count = js["favourite_count"]
        self.rating = js["rating"]
        self.download_unavailable = js["download_unavailable"]
        self.audio_unavailable = js["audio_unavailable"]
        self.playcount = js["playcount"]
        self.passcount = js["passcount"]
        self.max_combo = js["max_combo"]
        self.diff_aim = js["diff_aim"]
        self.diff_speed = js["diff_speed"]
        self.difficultyrating = js["difficultyrating"]
