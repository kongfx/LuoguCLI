#    LuoguCLI
#    Copyright (C) 2024-2025  ko114

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


from datetime import datetime

from .utils import _get, get_csrf_token, Session, _post
from .user import User


class Paste():
    """剪贴板

    :param str id: 剪贴板 ID

    :var str data: 内容
    :var str id: 剪贴板 ID
    :var User user: 用户
    :var datetime.datetime time: 时间
    :var bool public: 是否公开
    """

    def __init__(self, session: Session, id: str) -> None:
        self.session = session
        self._current_data: dict[str] = _get(session,
                                             f'Paste{id}'
                                             f"https://www.luogu.com.cn/paste/{id}"
                                             )["currentData"]

        paste: dict[str] = self._current_data["paste"]
        self.data: str = paste["data"]
        self.id: str = paste["id"]
        self._user: dict[str] = paste["user"]
        self.time = datetime.fromtimestamp(paste["time"])
        self.public: bool = paste["public"]

    @property
    @cached_method
    def user(self) -> User:
        return User(self._user["uid"])

    def delete(self) -> str:
        """删除剪贴板

        :returns: 剪贴板 ID
        :rtype: str
        """
        return _post(self.session, f"https://www.luogu.com.cn/paste/delete/{self.id}")["id"]

    def edit(self, data: str = None, public: bool = None):
        """编辑剪贴板

        :param str data: 剪贴板内容
        :param bool public: 是否公开

        :returns: 剪贴板 ID
        :rtype: str
        """
        r = _post(
            self.session,
            f"https://www.luogu.com.cn/paste/edit/{self.id}",
            {"data": data, "public": public},
        )
        if data is not None:
            self.data = data
        if public is not None:
            self.public = public
        return r["id"]

    @classmethod
    def new(cls, session, data: str, public: bool = None) -> "Paste":
        """新建剪贴板

        :param str data: 剪贴板内容
        :param bool public: 值为真时表示公开剪贴板，否则表示私有剪贴板

        :rtype: Session.Paste
        """
        r = _post(
            session,
            "https://www.luogu.com.cn/paste/new",
            {"data": data, "public": public},
        )
        return cls(r["id"])
