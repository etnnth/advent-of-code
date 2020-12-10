"""
Functions to fetch problem statement and data
"""

import requests
import os
from html.parser import HTMLParser
import re
from typing import List

REGEX = re.compile("(?s)\<article(.*?)\<\/article>(.*?)\<\/p>")
COOKIE = os.environ["AdventOfCodeCookie"]


def statement(year: int, day: int) -> List[str]:
    """
    Fetch the problem statement, return an array containing both part.
    """
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}", cookies={"session": COOKIE}
    )
    if response.status_code == 200:
        return [
            "<article" + "".join(t) + "</article>" for t in REGEX.findall(response.text)
        ]
    response.raise_for_status()
    return [""]


def data(year: int, day: int) -> str:
    """
    Fetch data return it as a string
    """
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": COOKIE}
    )
    if response.status_code == 200:
        return response.text.rstrip()
    response.raise_for_status()
    return ""
