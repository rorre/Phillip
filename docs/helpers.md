There are lots of helper functions in Phillip as it tries to have as little dependencies as possible.
This will help you access requests data from osu! and process them.

## osu! API

In this section we will only bring functions to help you with osu! API. (v1, obviously.)

!!! warning
    You need to provide your osu! API token to `APIKEY` variable
    ```python
    import phillip.helper

    phillip.helper.APIKEY = osu_token
    # do stuffs here...
    ```

---

::: phillip.helper.get_api
    :docstring:

---

::: phillip.helper.get_beatmap_api
    :docstring:

---

!!! info
    `phillip.helper.get_beatmap_api` is a shorthand of `phillip.helper.get_api(**kwargs)`

## osu!web

In this section, we will scrape the site in order to get data from osu!

!!! warning
    A throttler is auto initiated to rate limit your request to **2 requests/minute** 
    in order to avoid getting banned. You may play around with the code to work around this but in general this is **highly discouraged**.

### General endpoint

::: phillip.helper.get_discussion_json
    :docstring:

---

::: phillip.helper.get_users
    :docstring:

---

::: phillip.helper.nomination_history
    :docstring:

### Beatmapset events

::: phillip.event_helper.get_events
    :docstring:

## Discord Webhook

To help you generate webhooks, I have made an Aiess-styled webhook generator for events.

::: phillip.helper.gen_embed
    :docstring:

