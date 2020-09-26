There are lots of helper functions in Phillip as it tries to have as little dependencies as possible.
This will help you access requests data from osu! and process them.

## osu!v v1 API

In this section we will only bring functions to help you with osu! API. (v1, obviously.)

---

::: phillip.osu.old.APIClient

## osu!web

In this section, we will scrape the site in order to get data from osu!

!!! warning
    A throttler is automatically initiated to rate limit your request to **2 requests/minute** 
    in order to avoid getting IP banned. You may change this but in general this is **highly discouraged**.

---

::: phillip.osu.new.abstract.ABCClient

::: phillip.osu.new.WebClient

