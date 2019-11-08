# -*- coding: utf-8 -*-
"""
GhostWriter | https://ghostwriter.sh/

Copyright (C) 2019 Hiro <hiro@torproject.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from PyQt5 import QtCore, QtWidgets, QtGui

from ghostwriter import strings


class OpenProject():
    """
    Open a lektor project into the GUI
    """

    def __init__(self, base, project, parent):

        self.base = base
        self.project = project
        self.parent = parent

        project_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent,
            caption=strings._("gui_choose_folder"),
            options=QtWidgets.QFileDialog.ShowDirsOnly,
        )
        self.project.set_folder(project_folder)
        self.parent.project_status_label.setText("{}: {}".format(strings._("project_status_label", True), self.project.folder))
