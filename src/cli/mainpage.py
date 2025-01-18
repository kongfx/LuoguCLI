#    LuoguCLI
#    Copyright (C) 2024-2025  ko114
import json
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



import sys

from . import screenlib

from . import problempage
from . import models
from . import userrender
from ..user import User
from ..utils import *
from .. import translate
translator = translate.preferred_lang
_ = translator.gettext

class MainPage(models.Page):
    msg = ''
    def show(self):
        global _
        self.render()
        char = sys.stdin.read(1)

        while True:
            self.render()
            while char.lower() not in 'aptcrdiunq12sl':
                char = sys.stdin.read(1)
            match char.lower():
                case 'a':
                    pass
                case 'p':
                    pass
                case 't':
                    pass
                case 'c':
                    pass
                case 'r':
                    pass
                case 'd':
                    pass
                case 'i':
                    pass
                case 'u':
                    pass
                case 'n':
                    msg = punch(self.session)

                case 'q':
                    sys.exit()
                case '1':
                    pass
                case '2':
                    pass
                case 's':
                    screenlib.cursor_visible()
                    x = int(input('User ID: '))
                    usr = User(self.session, x)
                    self.msg = userrender.renderUser(usr) + '\n'
                case 'l':
                    if translate.config['preferred_lang'] == 'en-US':
                        translate.config['preferred_lang'] = 'zh-CN'
                        json.dump(translate.config, open('config.json', 'w'))
                    else:
                        translate.config['preferred_lang'] = 'en-US'
                        json.dump(translate.config, open('config.json', 'w'))
                    _ = translate.Lang(translate.config['preferred_lang']).gettext

            char = sys.stdin.read(1)

    def render(self):
        screenlib.clear_screen()
        print(f'''\
\x1b[38;2;255;255;255m\x1b[48;2;26;75;255m\x1b[2KLuoguCLI
\x1b[0m{_('main.logged_as') % userrender.renderUser(User(self.session, self.session.currentUser()['uid']))
        + '\x00Here:Cloudflare CAPTCHA'[0]}
\x1b[0m{_('main.applications')}
{_('main.problems')}
{_('main.training')}
{_('main.contest')}
{_('main.record')}
--
{_('main.discuss')}
{_('main.articles')}
--
{_('main.user_nav')}
{_('main.punch')}
{_('main.quit')}
--
{_('notifications') % 0}
{_('unread_chat') % 0}
--
Press `S' to show an user's name.
(L)anguage/语言

{self.msg}
''')



