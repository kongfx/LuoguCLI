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


import os
import sys

'''
BoxDrawing:
┌ └ ┐ ┘ ┼ ┬ ┴ ├ ┤ ─ │ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ╛ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧ ╨ ╤ ╥ ╙ ╘ ╒ ╓ ╫ ╪ ━ ┃ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ┍ ┎ ┏ ┑ ┒ ┓ ┕ ┖ ┗ ┙ 
┚ ┛ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┥ ┦ ┧ ┨ ┩ ┪ ┫ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍ ╎ ╏ ╭ ╮ ╯ ╰ ╱ ╲ ╳ ╴ ╵ ╶ ╷ 
╸ ╹ ╺ ╻ ╼ ╽ ╾ ╿

'''


def powerline_left_output(blocks, colors):
    for (idx, block), (r, g, b) in zip(enumerate(blocks), colors):
        try:
            next_color = colors[idx + 1]
            flag = True
        except IndexError:
            next_color = (0, 0, 0)
            flag = False
        sys.stdout.write(f'\x1b[48;2;{r};{g};{b}m{block}\x1b[38;2;{r};{g};{b}m'
                         f'\x1b[48;2;'
                         f'{next_color[0]};{next_color[1]};{next_color[2]}m'
                         f'\x1b[0m' if flag else f'\x1b[48;2;'
                                                  f'{r};{g};{b}m'
                                                  f'{block}'
                                                  f'\x1b[0m'
                                                  f'\x1b[38;2;'
                                                  f'{r};{g};{b}m'
                                                  f'')
    sys.stdout.write('\x1b[0m\n')

def powerline_right_output(blocks, colors):
    for (idx, block), (r, g, b) in zip(enumerate(blocks), colors):
        try:
            next_color = colors[idx + 1]
            flag = True
        except IndexError:
            next_color = (0, 0, 0)
            flag = False
        sys.stdout.write(f'\x1b[48;2;{r};{g};{b}m{block}\x1b[38;2;{r};{g};{b}m'
                         f'\x1b[48;2;'
                         f'{next_color[0]};{next_color[1]};{next_color[2]}m'
                         f'\x1b[0m' if flag else f'\x1b[48;2;'
                                                  f'{r};{g};{b}m'
                                                  f'{block}'
                                                  f'\x1b[0m'
                                                  f'\x1b[38;2;'
                                                  f'{r};{g};{b}m'
                                                  f'')
    sys.stdout.write('\x1b[0m\n')


def powerline_left_output_nocolor(blocks):
    sys.stdout.write('\x1b[2m')
    blocks = [str(i) for i in blocks]
    sys.stdout.write(''.join(blocks))
    sys.stdout.flush()

def powerline_right_output_nocolor(blocks):
    blocks = [str(i) for i in blocks]
    sys.stdout.write(''.join(blocks))
    sys.stdout.flush()





def clear_screen():
    sys.stdout.write('\x1b[2J\x1b[H')
    sys.stdout.flush()


def move_cursor(x=1, y=1, absolute=True):
    if absolute:
        sys.stdout.write(f'\x1b[{y};{x}H')
    else:
        if y < 0:
            sys.stdout.write(f'\x1b[{abs(y)}A')
        else:
            sys.stdout.write(f'\x1b[{y}B')
        if x < 0:
            sys.stdout.write(f'\x1b[{abs(x)}D')
        else:
            sys.stdout.write(f'\x1b[{x}C')
    sys.stdout.flush()


def init():
    sys.stdout.write('\x1b[?47h\x1b[?1049h')

    clear_screen()
    move_cursor()


def erase_line(mode=0):
    sys.stdout.write(f'\x1b[{mode}K')
    sys.stdout.flush()


def reset_color():
    sys.stdout.write('\x1b[0m')

    sys.stdout.flush()


def on_exit():
    clear_screen()
    move_cursor()
    sys.stdout.write('\x1b[?47l\x1b[?1049l')


def strRGBfgcolors(color: tuple[int, int, int]):
    return f'\x1b[38;2;{color[0]};{color[1]};{color[2]}m'


def str256fgcolors(color):
    return f'\x1b[38;5;{color}m'


class FGColorCodes:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'

    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def str256bgcolors(color):
    return f'\x1b[48;5;{color}m'


def strRGBbgcolors(color: tuple[int, int, int]):
    return f'\x1b[48;2;{color[0]};{color[1]};{color[2]}m'


class BGColorCodes:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    DEFAULT = '\033[49m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def cursor_invisible():
    sys.stdout.write('\x1b[?25l')

    sys.stdout.flush()

def cursor_visible():
    sys.stdout.write('\x1b[?25h')
    sys.stdout.flush()

class TerminalMode:
    BOLD = '\033[1m'
    FAINT = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    INVERT = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    DOUBLE_UNDERLINE = '\033[21m'
    TOPLINE = '\033[53m'
    RESET_TOPLINE = '\033[55m'
    RESET_BOLD = '\033[22m'
    RESET_FAINT = '\033[22m'
    RESET_ITALIC = '\033[23m'
    RESET_UNDERLINE = '\033[24m'
    RESET_BLINK = '\033[25m'
    RESET_INVERT = '\033[27m'
    RESET_HIDDEN = '\033[28m'
    RESET_STRIKE = '\033[29m'
