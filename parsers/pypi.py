import time
import json
from datetime import date, timedelta

import grequests as req
from bs4 import BeautifulSoup

LINKS = {
    "disnake": ("https://pypistats.org/packages/disnake",
                "https://api.pepy.tech/api/v2/projects/disnake"),

    "nextcord": ("https://pypistats.org/packages/nextcord",
                 "https://api.pepy.tech/api/v2/projects/nextcord"),

    "pycord": ("https://pypistats.org/packages/py-cord",
               "https://api.pepy.tech/api/v2/projects/py-cord"),

    "discord.py": ("https://pypistats.org/packages/discord.py",
                   "https://api.pepy.tech/api/v2/projects/discord.py"),

    "interactions.py": ("https://pypistats.org/packages/discord-py-interactions",
                        "https://api.pepy.tech/api/v2/projects/discord-py-interactions"),
}

def parsing_pypi(library: str):

    link_get = [req.get(link) for link in LINKS[library]]
    responses = req.map(link_get)

    soup1 = BeautifulSoup(responses[0].content, 'html.parser')
    reqs = responses[1].text
    reqs = json.loads(reqs)

    div1 = soup1.find("div", {"class": "wrapper"}).text.split()
    last_day = str(date.today() - timedelta(days=1))

    downloads_list = reqs["downloads"][last_day]
    items_list = list(downloads_list.values())

    last_version2 = reqs['versions']
    last_version2.sort(key=lambda x: tuple((x.lstrip("v") + "z").split(".")))
    last_version2 = last_version2[-1]

    if library == "disnake":

        return {

            "last_version": div1[29],
            "downloads": div1[57::4],

        }, {

            "last_version": last_version2,
            "total_downloads": "{:,}".format(reqs['total_downloads']),
            "downloads_sum": "{:,}".format(sum(items_list)),
            "last_version_downloads": "{:,}".format(downloads_list[last_version2]),
            "set": last_day,

        }

    elif library == "nextcord":

        return {

            "last_version": div1[33],
            "downloads": div1[37::4],

        }, {

            "last_version": last_version2,
            "total_downloads": "{:,}".format(reqs['total_downloads']),
            "downloads_sum": "{:,}".format(sum(items_list)),
            "last_version_downloads": "{:,}".format(downloads_list[last_version2]),
            "set": last_day

        }

    elif library == "pycord":

        return {

            "last_version": div1[29],
            "downloads": div1[51::4][1:],

        }, {

            "last_version": last_version2,
            "total_downloads": "{:,}".format(reqs['total_downloads']),
            "downloads_sum": "{:,}".format(sum(items_list)),
            "last_version_downloads": "{:,}".format(downloads_list[last_version2]),
            "set": last_day

        }

    elif library == "discord.py":

        return {

            "last_version": div1[28],
            "downloads": div1[40::4][1:]

        }, {

            "last_version": last_version2,
            "total_downloads": "{:,}".format(reqs['total_downloads']),
            "downloads_sum": "{:,}".format(sum(items_list)),
            "last_version_downloads": "{:,}".format(downloads_list[last_version2]),
            "set": last_day

        }

    elif library == "interactions.py":

        return {

            "last_version": div1[33],
            "downloads": div1[51::4][1:]

        }, {

            "last_version": last_version2,
            "total_downloads": "{:,}".format(reqs['total_downloads']),
            "downloads_sum": "{:,}".format(sum(items_list)),
            "last_version_downloads": "{:,}".format(downloads_list[last_version2]),
            "set": last_day

        }
