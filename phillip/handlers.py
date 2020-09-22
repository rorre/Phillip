from pyee import AsyncIOEventEmitter

from phillip.abc import EventBase
from phillip.application import Phillip
from phillip.osu.classes.web import GroupUser


class Handler:
    """Handler base for ``Phillip``

    **Parameters:**

    * webhook_url - `str` -- Discord webhook url to send
    """

    def __init__(self):
        self.app: Phillip

    def register_emitter(self, emitter: AsyncIOEventEmitter):
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

    async def on_map_event(self, event: EventBase):
        """Function to be called when any beatmap event happens.
        """
        pass

    async def on_map_bubbled(self, event: EventBase):
        """Function to be called when a beatmap is bubbled.
        """
        pass

    async def on_map_qualified(self, event: EventBase):
        """Function to be called when a beatmap is qualified.
        """
        pass

    async def on_map_disqualified(self, event: EventBase):
        """Function to be called when a beatmap is disqualified.
        """
        pass

    async def on_map_popped(self, event: EventBase):
        """Function to be called when a beatmap is popped.
        """
        pass

    async def on_map_ranked(self, event: EventBase):
        """Function to be called when a beatmap is ranked.
        """
        pass

    async def on_map_loved(self, event: EventBase):
        """Function to be called when a beatmap is loved.
        """
        pass

    async def on_group_added(self, user: GroupUser):
        """Function to be called when someone gets added to a group.
        """
        pass

    async def on_group_removed(self, user: GroupUser):
        """Function to be called when someone gets removed from a group.
        """
        pass

    async def on_group_probation(self, user: GroupUser):
        """Function to be called when someone gets added/removed to/from the probation.
        """

    async def on_group_gmt(self, user: GroupUser):
        """Function to be called when someone gets added/removed to/from GMT.
        """
        pass

    async def on_group_bng(self, user: GroupUser):
        """Function to be called when someone gets added/removed to/from  BNG.
        """
        pass

    async def on_group_nat(self, user: GroupUser):
        """Function to be called when someone gets added/removed to/from NAT.
        """
        pass

    async def on_group_alumni(self, user: GroupUser):
        """Function to be called when someone gets added/removed to/from Alumni.
        """
        pass
