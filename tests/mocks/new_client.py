from unittest import mock

from bs4 import BeautifulSoup

with open("tests/mocks/web_mocks.html") as f:
    html_text = f.read()
    html_soup = BeautifulSoup(html_text, features="html.parser")

html_mock = mock.AsyncMock(return_value=html_soup)
