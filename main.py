# -*- coding: utf-8 -*-
# PEP8:NO, LINT:OK, PY3:NO


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Ninja HTML to CSS "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 30/10/2013 '
__prj__ = ' '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from BeautifulSoup import BeautifulSoup
from os import linesep
import re
from sets import Set

from PyQt4.QtGui import QIcon, QAction, QInputDialog

from ninja_ide.core import plugin


# constants
css_template = "{}{}{}{}{}{}{}{}{}"


###############################################################################


class Css_Builder(object):
    ' class to build CSS3 from HTML5 '
    css = ''

    def __init__(self, html):
        ' init class '
        indnt = ' ' * int(QInputDialog.getInteger(None, __doc__,
                          " CSS Indentation Spaces: ", 4, 0, 8, 2)[0])
        self.soup = BeautifulSoup(BeautifulSoup(html).prettify())
        previously_styled, css = ['head'], '@charset "utf-8";{}'.format(linesep)
        for part in self.get_tags():
            if part not in previously_styled:
                css += '{}{}{}{}{}{}{}'.format(part, '{', linesep,
                                               indnt, linesep, '}', linesep)
                previously_styled.append(part)

        for part in self.get_ids():
            if part not in previously_styled:
                css += '/* {} */{}'.format('_'.join(part).lower(), linesep)
                css += css_template.format(part[0], '#', part[1], '{', linesep,
                                           indnt, linesep, '}', linesep)
                previously_styled.append(part)

        for part in self.get_classes():
            if part not in previously_styled:
                css += '/* {} */{}'.format('_'.join(part).lower(), linesep)
                css += css_template.format(part[0], '.', part[1], '{', linesep,
                                           indnt, linesep, '}', linesep)
                previously_styled.append(part)
        self.css = css.strip()

    def get_tags(self):
        " get all tags in the html "
        raw_tags, tags = self.soup.findAll(re.compile('')), []
        for tag in raw_tags:
            tags.append((tag.name))
        return list(Set(tags))

    def get_classes(self):
        " get all classes in the html "
        raw_tags = self.soup.findAll(re.compile(''), {'class': re.compile('')})
        tags = []
        for tag in raw_tags:
            attrs_dict = {}
            for attr in tag.attrs:
                attrs_dict[attr[0]] = attr[1]
            tags.append((tag.name, attrs_dict['class']))
        return sorted(list(Set(tags)))

    def get_ids(self):
        " get all ids in the html "
        raw_tags = self.soup.findAll(re.compile(''), {'id': re.compile('')})
        tags = []
        for tag in raw_tags:
            attrs_dict = {}
            for attr in tag.attrs:
                attrs_dict[attr[0]] = attr[1]
            tags.append((tag.name, attrs_dict['id']))
        return sorted(list(Set(tags)))


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        super(Main, self).initialize(*args, **kwargs)
        self.locator.get_service("menuApp").add_action(QAction(QIcon.fromTheme("edit-select-all"), "HTML to CSS", self, triggered=lambda: self.locator.get_service("editor").add_editor(content=Css_Builder(str(self.locator.get_service("editor").get_actual_tab().textCursor().selectedText().encode("utf-8").strip()).lower()).css, syntax='css')))


###############################################################################


if __name__ == "__main__":
    print(__doc__)
