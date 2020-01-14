from phillip import helper
import aiohttp

class Handler:
    """Handler base for ``Phillip``

    **Parameters:**

    * webhook_url - `str` -- Discord webhook url to send
    """

    def __init__(self, webhook_url):
        self.hook_url = webhook_url

    def register_emitter(self, emitter):
        """Registers an emitter to the handler

        **Parameters:**

        * emitter - `pyee.AsyncIOEventEmitter` -- Emitter to register.
        """
        self.emitter = emitter
        self._register_events()

    def _register_events(self):
        for func in dir(self):
            if not func.startswith("on_"):
                continue
            if func == "on_map_event":
                self.emitter.on("map_event", getattr(self, func))
            elif func == "on_group_added":
                self.emitter.on("group_added", getattr(self, func))
            elif func == "on_group_removed":
                self.emitter.on("group_removed", getattr(self, func))
            elif func == "on_group_probation":
                self.emitter.on("bng_limited", getattr(self, func))
            else:
                self.emitter.on(func.split("_")[-1], getattr(self, func))

    async def on_map_event(self, event):
        """Function to be called when any beatmap event happens.
        """
        pass

    async def on_map_bubbled(self, event):
        """Function to be called when a beatmap is bubbled.
        """
        pass

    async def on_map_qualified(self, event):
        """Function to be called when a beatmap is qualified.
        """
        pass

    async def on_map_disqualified(self, event):
        """Function to be called when a beatmap is disqualified.
        """
        pass

    async def on_map_popped(self, event):
        """Function to be called when a beatmap is popped.
        """
        pass

    async def on_map_ranked(self, event):
        """Function to be called when a beatmap is ranked.
        """
        pass

    async def on_map_loved(self, event):
        """Function to be called when a beatmap is loved.
        """
        pass

    async def on_group_added(self, user):
        """Function to be called when someone gets added to a group.
        """
        pass

    async def on_group_removed(self, user):
        """Function to be called when someone gets removed from a group.
        """
        pass

    async def on_group_probation(self, user):
        """Function to be called when someone gets added/removed to/from the probation.
        """

    async def on_group_gmt(self, user):
        """Function to be called when someone gets added/removed to/from GMT.
        """
        pass

    async def on_group_bng(self, user):
        """Function to be called when someone gets added/removed to/from  BNG.
        """
        pass

    async def on_group_nat(self, user):
        """Function to be called when someone gets added/removed to/from NAT.
        """
        pass

    async def on_group_alumni(self, user):
        """Function to be called when someone gets added/removed to/from Alumni.
        """
        pass

class SimpleHandler(Handler):
    async def on_map_event(self, event):
        """Parse beatmap event and send to discord webhook.

        **Parameters:**

        * event - `EventBase` -- The beatmapset event
        """
        embed = await helper.gen_embed(event)
        with aiohttp.ClientSession() as session:
            await session.post(self.hook_url, json={
                'content': event.event_source_url,
                'embeds': [embed]
            })
        return
