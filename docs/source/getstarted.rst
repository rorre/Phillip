.. currentmodule:: notAiess

Getting Started
===============

Installing
----------
To install, clone the repository, and install the packages needed from ``requirements.txt``

.. code-block:: sh

    $ git clone https://github.com/rorre/notAiess.github
    $ cd notAiess
    $ pip install -r requirements.txt

Example
-------
This is a very basic example of using ``notAiess`` to forward events to a discord hook.::

    from notAiess import notAiess
    nA = notAiess("0c38a********************", webhook_url="https://discordapp.com/api/webhooks/************")
    nA.run()

Advanced Usage
~~~~~~~~~~~~~~
This section will give you an example of using custom ``Handler`` to handle beatmap events.::

    from notAiess import notAiess, Handler
    from requests_async import requests
    class HandleMap(Handler):
        async def on_map_event(self, event):                       # Function to parse beatmap event
            embed = await helper.gen_embed(event)
            with aiohttp.ClientSession() as session:
                await session.post(self.hook_url, json={
                    'content': event.event_source_url,
                    'embeds': [embed]
                })                                                 # Send webhook to Discord

    nA = notAiess("0c38a********************", handlers=[HandleMap()])
    nA.run()
