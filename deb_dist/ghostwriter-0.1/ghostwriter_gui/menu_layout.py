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

class MenuLayout():
    """
    Add a menu layout into the GUI
    """
    def __init__(self, base, layout, main_window):
        self.base = base
        self.layout = layout
        self.main_window = main_window

        # Define menu buttons and labels

        self.open_label = QtWidgets.QLabel(strings._('button_open', True))
        self.open_label.setStyleSheet(self.base.css["menu_label"])
        self.open_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.open_label.setFixedHeight(50)
        self.open_button = QtWidgets.QPushButton();
        self.open_button.setFixedHeight(50)
        self.open_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/folder-3x.png"))
        )
        self.open_button.setStyleSheet(self.base.css["menu_button"])
        self.open_button.clicked.connect(main_window.open_button_clicked)

        self.close_label = QtWidgets.QLabel(strings._('button_close', True))
        self.close_label.setStyleSheet(self.base.css["menu_label"])
        self.close_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.close_label.setFixedHeight(50)
        self.close_button = QtWidgets.QPushButton();
        self.close_button.setFixedHeight(50)
        self.close_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/x-3x.png"))
        )
        self.close_button.setStyleSheet(self.base.css["menu_button"])
        self.close_button.clicked.connect(main_window.close_button_clicked)

        self.view_label = QtWidgets.QLabel(strings._('button_view', True))
        self.view_label.setStyleSheet(self.base.css["menu_label"])
        self.view_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.view_label.setFixedHeight(50)
        self.view_button = QtWidgets.QPushButton();
        self.view_button.setFixedHeight(50)
        self.view_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/eye-3x.png"))
        )
        self.view_button.setStyleSheet(self.base.css["menu_button"])
        self.view_button.clicked.connect(main_window.view_button_clicked)

        self.edit_label = QtWidgets.QLabel(strings._('button_edit', True))
        self.edit_label.setStyleSheet(self.base.css["menu_label"])
        self.edit_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.edit_label.setFixedHeight(50)
        self.edit_button = QtWidgets.QPushButton();
        self.edit_button.setFixedHeight(50)
        self.edit_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/pencil-3x.png"))
        )
        self.edit_button.setStyleSheet(self.base.css["menu_button"])
        self.edit_button.clicked.connect(main_window.edit_button_clicked)

        self.push_label = QtWidgets.QLabel(strings._('button_push', True))
        self.push_label.setStyleSheet(self.base.css["menu_label"])
        self.push_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.push_button = QtWidgets.QPushButton();
        self.push_button.setFixedHeight(50)
        self.push_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/data-transfer-upload-3x.png"))
        )
        self.push_button.setStyleSheet(self.base.css["menu_button"])
        self.push_button.clicked.connect(main_window.push_button_clicked)

        self.sync_label = QtWidgets.QLabel(strings._('button_sync', True))
        self.sync_label.setStyleSheet(self.base.css["menu_label"])
        self.sync_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.sync_label.setFixedHeight(50)
        self.sync_button = QtWidgets.QPushButton();
        self.sync_button.setFixedHeight(50)
        self.sync_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/reload-3x.png"))
        )
        self.sync_button.setStyleSheet(self.base.css["menu_button"])
        self.sync_button.clicked.connect(main_window.sync_button_clicked)

        self.rebase_label = QtWidgets.QLabel(strings._('button_rebase', True))
        self.rebase_label.setStyleSheet(self.base.css["menu_label"])
        self.rebase_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.rebase_label.setFixedHeight(50)
        self.rebase_button = QtWidgets.QPushButton();
        self.rebase_button.setFixedHeight(50)
        self.rebase_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/fork-3x.png"))
        )
        self.rebase_button.setStyleSheet(self.base.css["menu_button"])
        self.rebase_button.clicked.connect(main_window.rebase_button_clicked)

        self.onion_label = QtWidgets.QLabel(strings._('button_onion', True))
        self.onion_label.setStyleSheet(self.base.css["menu_label"])
        self.onion_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.onion_label.setFixedHeight(50)
        self.onion_button = QtWidgets.QPushButton();
        self.onion_button.setFixedHeight(50)
        self.onion_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/shield-3x.png"))
        )
        self.onion_button.setStyleSheet(self.base.css["menu_button"])
        self.onion_button.clicked.connect(main_window.onion_button_clicked)

        self.settings_label = QtWidgets.QLabel(strings._('button_settings', True))
        self.settings_label.setStyleSheet(self.base.css["menu_label"])
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.settings_label.setFixedHeight(50)
        self.settings_button = QtWidgets.QPushButton();
        self.settings_button.setFixedHeight(50)
        self.settings_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/cog-3x.png"))
        )
        self.settings_button.setStyleSheet(self.base.css["menu_button"])
        self.settings_button.clicked.connect(main_window.settings_button_clicked)

        # Define menu panel
        self.labels_layout = QtWidgets.QHBoxLayout()
        self.labels_layout.setSpacing(0)
        self.labels_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QtWidgets.QHBoxLayout()
        self.panel_layout.setSpacing(0)
        self.panel_layout.setContentsMargins(0, 0, 0, 0)

        # Add labels to panel
        self.labels_layout.addWidget(self.open_label)
        self.labels_layout.addWidget(self.close_label)
        self.labels_layout.addWidget(self.view_label)
        self.labels_layout.addWidget(self.edit_label)
        self.labels_layout.addWidget(self.push_label)
        self.labels_layout.addWidget(self.sync_label)
        self.labels_layout.addWidget(self.rebase_label)
        self.labels_layout.addWidget(self.onion_label)
        self.labels_layout.addWidget(self.settings_label)

        # Add buttons to panel
        self.panel_layout.addWidget(self.open_button)
        self.panel_layout.addWidget(self.close_button)
        self.panel_layout.addWidget(self.view_button)
        self.panel_layout.addWidget(self.edit_button)
        self.panel_layout.addWidget(self.push_button)
        self.panel_layout.addWidget(self.sync_button)
        self.panel_layout.addWidget(self.rebase_button)
        self.panel_layout.addWidget(self.onion_button)
        self.panel_layout.addWidget(self.settings_button)

        self.layout.addLayout(self.labels_layout)
        self.layout.addLayout(self.panel_layout)
