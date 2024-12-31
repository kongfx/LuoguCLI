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

# Entrypoint for LuoguCLI.
import atexit
import sys
import os
import termios
import tty




from . import screenlib
from . import mainpage
from . import models
from .. import utils

dbg = True

class FirstPage(models.Page):
    def render(self):
        print('''\
LuoguCLI  Copyright (C) 2024-2025  ko114
This program comes with ABSOLUTELY NO WARRANTY; for details type `w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `c' for details. 
Press Enter to continue. Press Ctrl-C to quit.
        ''')



    def show(self):
        try:
            screenlib.init()
            old_tcsetting = termios.tcgetattr(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            if not dbg:  # debug
                atexit.register(screenlib.on_exit)
                screenlib.cursor_invisible()
                def onexit(*args):
                    screenlib.cursor_visible()
                    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_tcsetting)

                atexit.register(onexit)
            screenlib.move_cursor()
            self.render()
            char = sys.stdin.read(1)

            while char != '\n':
                if char == 'w':
                    os.system(f'{os.environ.get("PAGER", "more")} cli/warranty.txt')
                    screenlib.init()
                    self.render()
                elif char == 'c':
                    os.system(f'{os.environ.get("PAGER", "more")} cli/copyright.txt')
                    screenlib.init()
                    self.render()
                char = sys.stdin.read(1)
            page = mainpage.MainPage(session=self.session)
            page.show()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    firstpage = FirstPage(utils.Session(utils._cookies))
    firstpage.show()
