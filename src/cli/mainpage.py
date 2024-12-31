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



import sys

from . import screenlib

from . import problempage
from . import models
from . import userrender
from ..user import User

class MainPage(models.Page):
    def show(self):
        self.render()

    def render(self):
        screenlib.clear_screen()
        print(f'''\
\x1b[38;2;255;255;255m\x1b[48;2;26;75;255m\x1b[2KLuoguCLI
\x1b[0mLogged as {userrender.renderUser(User(self.session, self.session.currentUser()['uid']))}
\x1b[0m\x1b[4mA\x1b[0mpplications
\x1b[4mP\x1b[0mroblems
\x1b[4mT\x1b[0mraining
\x1b[4mC\x1b[0montest
\x1b[4mR\x1b[0mecord
--
\x1b[4mD\x1b[0miscuss
Art\x1b[4mi\x1b[0mcles
--
\x1b[4mU\x1b[0mser Nav
Pu\x1b[4mn\x1b[0mch
\x1b[4mQ\x1b[0muit
--
You have 0 notification(s) Press `1' to read.
You have 0 message(s) Press `2' to read.
''')
        char = sys.stdin.read(1)
        while char.lower() not in 'aptcrdiunq12':
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
                pass
            case 'q':
                sys.exit()
            case '1':
                pass
            case '2':
                pass

