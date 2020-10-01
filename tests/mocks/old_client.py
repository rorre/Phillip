import json

with open("tests/mocks/api_mocks.json") as f:
    MAP_JSONS = json.load(f)


async def get_api(_, **kwargs):
    return MAP_JSONS[str(kwargs["s"])]
