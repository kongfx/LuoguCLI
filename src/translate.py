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

config = open('config.json', 'r').read()
config = json.loads(config)

class Lang:
    def __init__(self, lang_code: str):
        self._lang = lang_code
        self._words = open(f'assets/lang/{lang_code}.json').read()
        self._words = json.loads(self._words)

    def gettext(self, c: str):
        return self._words.get(c, c)


preferred_lang = Lang(config['preferred_lang'])