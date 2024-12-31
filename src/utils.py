#    LuoguCLI
#    Copyright (C) 2024-2525  ko114

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import hashlib
import json
import os
from datetime import datetime
from html.parser import HTMLParser
from http.cookies import SimpleCookie
from io import BytesIO
import requests
from tqdm.auto import tqdm

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Referer": "https://www.luogu.com.cn/",
    "X-Luogu-Type": "content-only",
    "X-Lentille-Request": "content-only",
}
_cookies = {'_uid': '1435654', '__client_id': '19a30a48f4ba8b10000df027df5b87b2d56c5fe6'}


def get_csrf_token(
        session: requests.Session, url: str = "https://www.luogu.com.cn/"
) -> str:
    class HTMLCSRFTokenParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            try:
                if tag == "meta" and attrs["name"] == "csrf-token":
                    raise StopIteration(attrs["content"])
            except KeyError:
                pass

    r = session.get(url)
    r.raise_for_status()
    try:
        HTMLCSRFTokenParser().feed(r.text)
    except StopIteration as csrf_token:
        return str(csrf_token)


def _get(session: 'Session', name, url, forceDownload=False):
    if os.path.exists(f'../data/{name}.json') and not forceDownload:
        with open(f'../data/{name}.json', 'r') as f:
            return json.load(f)

    def download(url):
        response = session.session.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        with open(f'../data/{name}.json', 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading {name}.json...',
                      disable=False) as pbar:
                for data in response.iter_content(block_size):
                    pbar.update(len(data))
                    file.write(data)

    download(url)
    return json.load(open(f'../data/{name}.json', 'r'))


def _post(session: 'Session', url, data):
    hash = hashlib.md5((url + data).encode('utf-8')).hexdigest()

    def download(url):
        nonlocal hash, data
        response = session.session.post(url, hash, stream=True, json=data)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        with open(f'../data/{hash}.json', 'wb') as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading {hash}.json...',
                      disable=False) as pbar:
                for data in response.iter_content(block_size):
                    pbar.update(len(data))
                    file.write(data)

    download(url)
    return json.load(open(f'../data/{name}.json', 'r'))


class Session:
    """会话

    :param cookies: Cookies
    :type cookies: str | dict[str, str] | None

    :var requests.cookies.RequestsCookieJar cookies: Cookies
    :var requests.Session session: 会话
    """

    def __init__(self, cookies: str | dict[str, str] | None = None) -> None:
        self.cookies = requests.cookies.cookiejar_from_dict(
            {k: v.value for k, v in SimpleCookie(cookies).items()}
        )
        self.session = requests.Session()
        self.session.headers.update(headers)

        self.session.cookies = self.cookies

    def captcha(self, show: bool = True) -> bytes:
        """获取验证码

        :param bool show:
            值为真时使用 :meth:`PIL.Image.Image.show` 显示验证码；否则仅返回图片的二进制数据

        :rtype: bytes
        """
        r = self.session.get("https://www.luogu.com.cn/api/verify/captcha")
        r.raise_for_status()
        if show:
            from PIL import Image

            Image.open(BytesIO(r.content)).show(title="CAPTCHA")
        return r.content

    def login(self, username: str, password: str, captcha: str) -> "dict[str]":
        """登录

        :param str username: 用户名
        :param str password: 密码
        :param str captcha: 验证码

        :rtype: dict[str]
        """

        r = self.session.post(
            "https://www.luogu.com.cn/api/auth/userPassLogin",
            headers={
                "x-csrf-token": get_csrf_token(
                    self.session, "https://www.luogu.com.cn/auth/login"
                ),
            },
            json={
                "username": username,
                "password": password,
                "captcha": captcha,
            },
        )
        #r.raise_for_status()
        return r.json()

    def logout(self) -> "dict[str, bool]":
        """登出

        :rtype: dict[str, bool]
        """
        r = self.session.post(
            "https://www.luogu.com.cn/api/auth/logout",
            headers={"x-csrf-token": get_csrf_token(self.session)},
        )
        r.raise_for_status()
        return r.json()

    def changeSlogan(self, newSlogan:str):
        r=self.session.post(
            'https://www.luogu.com.cn/api/user/updateSlogan',
            headers={"x-csrf-token": get_csrf_token(self.session)},
            json={'slogan': newSlogan}
        )
        r.raise_for_status()

    def changeLastOnline(self):
        fmt = '%Y-%m-%d %H:%M'
        last = len('YYYY-MM-DD HH:mm')
        now = datetime.now()
        s = self.currentUser()['slogan']
        print(s)
        f = now.strftime(fmt)
        newSlogan = s[:-16] + f
        print(newSlogan)
        self.changeSlogan(newSlogan)

    def currentUser(self) -> dict:
        return self.session.post('https://www.luogu.com.cn/problem/list').json()['currentUser']



def cached_method(func):
    def wrapper(self, *args):
        if not hasattr(self, "__cache"):
            self.__cache = {}
        cache = self.__cache
        if args not in cache:
            cache[args] = func(self, *args)
        return cache[args]

    return wrapper


class LazyList(list):
    def __init__(self, model, args):
        super().__init__(args)
        self._model = model

    @cached_method
    def __getitem__(self, index):
        return self._model(super().__getitem__(index))

    def __iter__(self):
        for i in super().__iter__():
            yield self._model(i)

    def __repr__(self) -> str:
        return (
                "["
                + ",\n ".join([f"{self._model.__name__}({i})" for i in list.__iter__(self)])
                + "]"
        )


def dict_without_underscores(d: dict):
    return dict(filter(lambda i: not i[0].startswith("_"), d.items()))


def punch(session: Session):
    req = session.session.post("https://www.luogu.com.cn/index/ajax_punch")
    json_data = req.json()
    if req.status_code != 200:
        return json_data['message']
    else:
        return json_data['more']['html']