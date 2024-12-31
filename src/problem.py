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


import os.path
from datetime import datetime

import requests, json
from tqdm.auto import tqdm

import utils

from utils import get_csrf_token, cached_method

#cookies={}
from utils import _get


def list(session: utils.Session):
    url = "https://www.luogu.com.cn/problem/list"
    return _get(session, "problems", url)


class Problem:
    def __init__(self, session: utils.Session, pid: str):
        self.session = session
        self.pid = pid
        self._url = "https://www.luogu.com.cn/problem/" + self.pid
        self._data = _get(session, self.pid, self._url)['currentData']
        self.background = self._data['problem']['background']
        self.title = self._data['problem']['title']
        self.description = self._data['problem']['description']
        self.hint = self._data['problem']['hint']
        self.totalSubmit = self._data['problem']['totalSubmit']
        self.totalAccepted = self._data['problem']['totalAccepted']
        self.totalRejected = self.totalSubmit - self.totalAccepted
        self.score = self._data['problem']['score']
        self.accepted = self.score == self.full_score
        self.passingRate = self.totalAccepted / self.totalSubmit * 100
        problem: dict[str] = self._data["problem"]
        self.input_format: str = problem["inputFormat"]
        self.output_format: str = problem["outputFormat"]
        self.samples: list[tuple[str, str]] = [(s[0], s[1]) for s in problem["samples"]]
        self._provider: str = problem["provider"]
        self.attachments = [
            self.Attachment(**attachment) for attachment in problem["attachments"]
        ]
        self.can_edit: bool = problem["canEdit"]
        self.limits: dict[str, list[int]] = problem["limits"]
        self.std_code: str = problem["stdCode"]
        self.tags: list[int] = problem["tags"]
        self.wants_translation: bool = problem["wantsTranslation"]
        self.flag: int = problem["flag"]
        self.difficulty: int = problem["difficulty"]
        self.full_score: int = problem["fullScore"]
        self.type: str = problem["type"]
        # print(f'通过率 {self.passingRate:.2f}%')

    def submit(self, code: str, enableO2: bool, lang: int):
        return self.session.session.post(f'https://www.luogu.com.cn/fe/api/problem/submit/{self.pid}',
                                  json={
                                            'code': code,
                                            'enableO2': enableO2,
                                            'lang': lang
                                       }
                                  ).json()['rid']

    class Attachment():
        """附件

        :var str download_link: 下载链接
        :var int size: 大小
        :var datetime.datetime upload_time: 上传时间
        :var str id: ID
        :var str filename: 文件名
        """

        def __init__(
                self,
                downloadLink: str,
                size: int,
                uploadTime: int,
                id: str,
                filename: str,
        ) -> None:
            self.download_link = downloadLink
            self.size = size
            self.upload_time = datetime.fromtimestamp(uploadTime)
            self.id = id
            self.filename = filename

    @property
    def id(self):
        return self.pid

    @property
    @cached_method
    def provider(self):
        from user import User
        return User(self._provider["uid"])
