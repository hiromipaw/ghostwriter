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

from ghostwriter import strings

from PyQt5 import QtCore, QtWidgets, QtGui

class ProjectLayout():
    """
    Add a project layout into the GUI
    """
    def __init__(self, base, layout, main_window):
        self.base = base
        self.layout = layout
        self.main_window = main_window

        self.project_layout = QtWidgets.QHBoxLayout()
        self.project_layout.setSpacing(0)
        self.project_layout.setContentsMargins(0, 0, 0, 0)

        # Define project status box
        self.project_status_label = QtWidgets.QLabel("{}: ".format(strings._('project_status_label', True)))
        self.project_status_label.setFixedHeight(50)
        self.project_status_label.setStyleSheet(
            self.base.css["project_status_indicator_label"]
        )

        # Add project status to panel
        self.project_layout.addWidget(self.project_status_label)

        self.layout.addLayout(self.project_layout)

        project_folder = self.base.settings.get("project_folder")
        if project_folder:
            self.set_project_label(project_folder)
            self.main_window.set_project(project_folder)
            self.main_window.start_web()


    def set_project_label(self, text):
        self.project_status_label.setText(text)
