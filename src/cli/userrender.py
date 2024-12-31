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


from ..user import *
from .screenlib import strRGBfgcolors, strRGBbgcolors
import requests

colormap={
    'Gray': strRGBfgcolors((191,191,191)),
    'Blue': strRGBfgcolors((14, 114, 210)),
    'Green': strRGBfgcolors((94,185,94)),
    'Orange': strRGBfgcolors((230,126,34)),
    'Red': strRGBfgcolors((231, 76, 60)),
    'Purple': strRGBfgcolors((142, 68, 173)),
    'Brown': strRGBfgcolors((173, 139, 0)),
    'GreenHanger': strRGBbgcolors((94, 185, 94)),
    'BlueHanger': strRGBbgcolors((52, 152, 219)),
    'GoldenHanger': strRGBbgcolors((241, 196, 15)),
}
def renderUser(user: User) -> str:
    color: str = colormap[user.color]

    badge = f'{color.replace("38;2", "48;2", 1)}\x1b[38;2;255;255;255m {user.badge} \x1b[0m' if user.badge else ''

    hanger = ''
    if user.ccf_level in range(3, 6):
        hanger = f'{colormap["GreenHanger"]}\x1b[38;2;255;255;255m {user.ccf_level} \x1b[0m'
    elif user.ccf_level in range(6, 8):
        hanger = f'{colormap["BlueHanger"]}\x1b[38;2;255;255;255m {user.ccf_level} \x1b[0m'
    elif user.ccf_level in range(8, 10):
        hanger = f'{colormap["GoldenHanger"]}\x1b[38;2;255;255;255m {user.ccf_level} \x1b[0m'
    # 这里为是否贡献者或支持者，显示粗斜体 Tag 贡献者

    rep = requests.get('https://kongfx.github.io/LuoguCLI/supportlist.json')
    is_sp = False
    if rep.status_code == 200:
        data = rep.json()
        if user.uid in data['data']:
            is_sp = True

    return (f'\x1b[1m{color}{user.name} {badge} \x1b[1m{hanger} '
            f'{f"""\x1b[1m\x1b[3m{color.replace("38;2", 
                                                "48;2",
                                                1)}\x1b[38;2;255;255;255m 支持者 """ if is_sp else ''}\x1b[0m')


