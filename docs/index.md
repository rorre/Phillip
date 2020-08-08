# Phillip

Phillip is an event driven osu! feed for Python. It is written on top of asyncio so it is running pretty fast.

## Features

* Asyncronous
* Event-driven API (Easy management for each events)
* Easy to use
* Rate limited to not get you banned from.peppy's server

## Requirements

* Python 3.6+

## Dependencies

* `pyee` - To fire events into handlers.
* `beautifulsoup4` - HTML parsing from osu! site.
* `aiohttp` - Asyncronously requests data from osu! site.
* `asyncio-throttle` - Rate limiting for web scraper.

## Installation

```
$ git clone https://github.com/rorre/Phillip.git
$ cd Phillip
$ python -m pip install .
```

PyPI release is planned.

## Example
### Discord Webhook

```python
from phillip.application import Phillip
p = Phillip(
    "0c38a********************", # osu! API token
    webhook_url="https://discordapp.com/api/webhooks/************" # Discord webhook URL
)
p.run()
```

### Advanced Usage
This section will give you an example of using custom ``Handler`` to handle beatmap events

```python
from phillip.application import Phillip
from phillip.handlers import Handler
import aiohttp

# Always inherit Handler class!
# It has some magic functions to register the event emitter so that listening function could work.
class HandleMap(Handler):
    # Function to handle every beatmap event.
    # To see other event handler you can add, see https://notaiess.readthedocs.io/en/latest/api.html#event-listener
    async def on_map_event(self, event):
        # Generate webhook dict of the event. This will be converted to JSON later.
        embed = await helper.gen_embed(event)

        # Send webhook with aiohttp.
        # It is better to use aiohttp as it's already embedded when you install notAiess.
        with aiohttp.ClientSession() as session:
            await session.post(self.hook_url, json={
                'content': event.event_source_url,
                'embeds': [embed]
            })

p = Phillip(
        "0c38a********************",
        handlers=[
            HandleMap("https://discordapp.com/api/webhooks/************")
        ]
    )
p.run()
```