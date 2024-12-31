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


from abc import ABC, abstractmethod
from ..utils import Session

class Page(ABC):
    def __init__(self, session: Session):
        self.session = session

    '''
    绘制页面。每一次操作完成应该调用。不做按键处理。
    '''
    @abstractmethod
    def render(self):
        raise NotImplementedError

    @abstractmethod
    def show(self):
        self.render()

