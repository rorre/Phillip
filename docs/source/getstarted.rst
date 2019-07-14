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

    from notAiess import notAiess, helper

    class HandleMap:
        def parse(event):                             # Required function to parse beatmap event
            embed = helper.gen_embed(event)           # Generate Discord embed
            hook_url = "https://discordapp.com/api/webhooks/************"
            requests.post(hook_url, json={
                'content': event.event_source_url,
                'embeds': [embed]
            })                                        # Send webhook to Discord

    nA = notAiess("0c38a********************", handlers=[HandleMap()])
    nA.run()
