import json
from unittest.mock import AsyncMock

from bs4 import BeautifulSoup

with open("tests/mocks/discord/api.json") as f:
    USERS_JSON = json.load(f)

with open("tests/mocks/discord/mocks.html") as f:
    MOCKS_SOUP = BeautifulSoup(f, "html.parser")

with open("tests/mocks/discord/pop_mock.html") as f:
    POP_SOUP = BeautifulSoup(f, "html.parser")

html_mock = AsyncMock(return_value=MOCKS_SOUP)
pop_mock = AsyncMock(return_value=POP_SOUP)
with open("tests/mocks/discord/map.json") as f:
    map_json = json.load(f)

with open("tests/mocks/discord/pop_map.json") as f:
    popped_map_json = json.load(f)


async def get_api(_, **kwargs):
    return USERS_JSON[str(kwargs["u"])]
