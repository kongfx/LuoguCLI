#!/usr/bin/env python3
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


import json
import sys


def formatJSON(data):
    return json.dumps(json.loads(data), indent=4)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fin:
        data = fin.read()
        open(sys.argv[1], 'w').write(formatJSON(data))
