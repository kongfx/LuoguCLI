#    LuoguCLI
#    Copyright (C) 2024-2025  ko114
import sys

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
from . import models
from .screenlib import *
from . import userrender
from ..user import User
from ..utils import *
from .. import translate
from .. import problem

translator = translate.preferred_lang
_ = translator.gettext
problem_diff = [
    {
        "id": 0,
        "name": "\u6682\u65e0\u8bc4\u5b9a",
        "color": (191, 191, 191)
    },
    {
        "id": 1,
        "name": "\u5165\u95e8",
        "color": (254, 76, 97)
    },
    {
        "id": 2,
        "name": "\u666e\u53ca\u2212",
        "color": (243,156,17)
    },
    {
        "id": 3,
        "name": "\u666e\u53ca/\u63d0\u9ad8\u2212",
        "color": (255, 193, 22)
    },
    {
        "id": 4,
        "name": "\u666e\u53ca+/\u63d0\u9ad8",
        "color": (82, 196, 26)
    },
    {
        "id": 5,
        "name": "\u63d0\u9ad8+/\u7701\u9009\u2212",
        "color": "blue-3"
    },
    {
        "id": 6,
        "name": "\u7701\u9009/NOI\u2212",
        "color": "purple-3"
    },
    {
        "id": 7,
        "name": "NOI/NOI+/CTSC",
        "color": "lapis-4"
    }
]


class ProblemPage(models.Page):
    def show(self):
        self.render()
        sys.stdin.read(1)


    def render(self):
        clear_screen()
        move_cursor()
        print(f'''\
\x1b[38;2;255;255;255m\x1b[48;2;26;75;255m\x1b[2KLuoguCLI
\x1b[0m{_('main.logged_as') % userrender.renderUser(User(self.session, self.session.currentUser()['uid']))
        + '\x00Here:Cloudflare CAPTCHA'[0]}
{_('problem.status')}\t{_('problem.title')}\t{_('problem.difficulty')}
''')
