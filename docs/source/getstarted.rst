.. currentmodule:: notAiess

Getting Started
===============

Installing
----------
To install, just install it with pip, really.

.. code-block:: sh

    $ pip install git+https://github.com/rorre/notAiess.git

PyPI release will happen someday.

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

    nA = notAiess(
            "0c38a********************",
            handlers=[
                HandleMap("https://discordapp.com/api/webhooks/************")
            ]
        )
    nA.run()
