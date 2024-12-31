from ..user import *
from .screenlib import strRGBfgcolors, strRGBbgcolors
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
    badge = f'{color.replace("38;2", "48;2", 1)}\x1b[38;3;255;255;255m {user.badge} \x1b[0m'
    hanger = ''
    if user.ccf_level in range(3, 6):
        hanger = f'{colormap["GreenHanger"]} {user.ccf_level} \x1b[0m'
    elif user.ccf_level in range(6, 8):
        hanger = f'{colormap["BlueHanger"]} {user.ccf_level} \x1b[0m'
    elif user.ccf_level in range(8, 10):
        hanger = f'{colormap["GoldenHanger"]} {user.ccf_level} \x1b[0m'
    is_sp = False  # 这里为是否贡献者或支持者，显示粗斜体 Tag 贡献者

