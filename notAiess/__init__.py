"""
notAiess
========

A basic wrapper for osu! beatmapset events
"""

from .__version__ import (__author__, __author_email__, __description__,
                          __license__, __title__, __url__, __version__)
from .abc import Handler
from .notaiess import SimpleHandler, helper, notAiess
