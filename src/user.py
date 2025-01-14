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

from .problem import Problem
from .utils import LazyList, cached_method, _get


# from . import Model


class User():
    """用户

    :param uid: 用户 ID
    :type uid: int | str

    :raises NotFoundHttpException: 用户未找到

    :var datetime.datetime register_time: 注册时间
    :var str introduction: 个人介绍
    :var list[Prize] prize: 获奖信息
    :var str blog_address: 个人博客地址
    :var passed_problem_count: 已通过题目数量
    :vartype passed_problem_count: int | None
    :var submitted_problem_count: 提交题目数量
    :vartype submitted_problem_count: int | None
    :var int uid: 用户 ID
    :var str name: 用户名
    :var str slogan: 个性签名
    :var badge: 徽章
    :vartype badge: str | None
    :var bool is_admin: 是否管理员
    :var bool is_banned: 是否被封禁
    :var str color: 颜色
    :var int ccf_level: CCF 等级
    :var int following_count: 关注数量
    :var int follower_count: 粉丝数量
    :var int ranking: 排名
    :var str background: 封面
    :var is_root: 是否为 root
    :vartype is_root: bool | None
    :var passed_problems: 已通过的题目
    :vartype passed_problems: list[Problem] | None
    :var submitted_problems: 尝试过的题目
    :vartype submitted_problems: list[Problem] | None
    """

    class Prize():
        """获奖信息

        :var int year: 年份
        :var str contest_name: 竞赛名称
        :var str prize: 奖项
        """

        def __init__(self, year: int, contestName: str, prize: str) -> None:
            self.year = year
            self.contest_name = contestName
            self.prize = prize

    def __init__(self, session, uid: "int | str") -> None:
        self.session = session
        self._current_data: dict[str] = _get(
            self.session,
            f'UserID{uid}',
            f"https://www.luogu.com.cn/user/{uid}"
        )["currentData"]

        user: dict[str] = self._current_data["user"]
        self.register_time = datetime.fromtimestamp(user["registerTime"])
        self.introduction: str = user["introduction"]
        self.prize = [self.Prize(**prize) for prize in user["prize"]]
        self.blog_address: str = user["blogAddress"]
        self.passed_problem_count: int | None = user["passedProblemCount"]
        self.submitted_problem_count: int | None = user["submittedProblemCount"]
        self.uid: int = user["uid"]
        self.name: str = user["name"]
        self.slogan: str = user["slogan"]
        self.badge: str | None = user["badge"]
        self.is_admin: bool = user["isAdmin"]
        self.is_banned: bool = user["isBanned"]
        self.color: str = user["color"]
        self.ccf_level: int = user["ccfLevel"]
        self.following_count: int = user["followingCount"]
        self.follower_count: int = user["followerCount"]
        self.ranking: int = user["ranking"]
        self.background: str = user["background"]
        self.is_root: bool = user["isRoot"] if "isRoot" in user else None

        self._passed_problems: list[dict] = (
            self._current_data["passedProblems"]
            if "passedProblems" in self._current_data
            else None
        )
        self.passed_problems: list[Problem] = (
            LazyList(
                Problem,
                [p["pid"] for p in self._passed_problems],
            )
            if self._passed_problems
            else []
        )
        self._submitted_problems: list[dict] = (
            self._current_data["submittedProblems"]
            if "submittedProblems" in self._current_data
            else None
        )
        self.submitted_problems: list[Problem] = (
            LazyList(
                Problem,
                [p["pid"] for p in self._submitted_problems],
            )
            if self._submitted_problems
            else []
        )

    @property
    def id(self):
        return self.uid

    @classmethod
    def search(cls, session, keyword: str) -> "list[User]":
        """根据 UID 或用户名搜索用户

        :param session:
        :param str keyword: 搜索关键字
        """
        users = _get(
            session,
            f"UserSearch{keyword}",
            f'https://www.luogu.com.cn/api/user/search?name={keyword}',
        )["users"]
        return LazyList(User, [u["uid"] for u in users if u is not None])
