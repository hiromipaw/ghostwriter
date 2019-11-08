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

from ghostwriter import strings
from ghostwriter.project import Project
from ghostwriter.web import Web
from .open_project import OpenProject

from PyQt5 import QtCore, QtWidgets, QtGui

class GhostWriterGui(QtWidgets.QMainWindow):
    """
    GhostWriterGui is the main window for the GUI that contains all of the
    GUI elements.
    """

    def __init__(self, base, qtapp):
        super(GhostWriterGui, self).__init__()

        self.qtapp = qtapp
        self.base = base

        self.base.log("GhostWriterGui", "__init__")

        self.setMinimumWidth(820)
        self.setMinimumHeight(660)

        self.setWindowTitle("GhostWriter")
        self.setWindowIcon(
            QtGui.QIcon(self.base.get_resource_path("images/ghostwriter.png"))
        )

        # System tray
        menu = QtWidgets.QMenu()
        self.settings_action = menu.addAction(strings._('gui_settings_window_title', True))
        exit_action = menu.addAction(strings._('systray_menu_exit', True))
        exit_action.triggered.connect(self.close)

        self.system_tray = QtWidgets.QSystemTrayIcon(self)
        # The convention is Mac systray icons are always grayscale
        if self.base.platform == 'Darwin':
            self.system_tray.setIcon(QtGui.QIcon(self.base.get_resource_path('images/ghostwriter-grayscale.png')))
        else:
            self.system_tray.setIcon(QtGui.QIcon(self.base.get_resource_path('images/ghostwriter.png')))
        self.system_tray.setContextMenu(menu)
        self.system_tray.show()

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
        self.open_button.clicked.connect(self.open_button_clicked)

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
        self.close_button.clicked.connect(self.close_button_clicked)

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
        self.view_button.clicked.connect(self.view_button_clicked)

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
        self.edit_button.clicked.connect(self.edit_button_clicked)

        self.push_label = QtWidgets.QLabel(strings._('button_push', True))
        self.push_label.setStyleSheet(self.base.css["menu_label"])
        self.push_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.push_button = QtWidgets.QPushButton();
        self.push_button.setFixedHeight(50)
        self.push_button.setIcon(
            QtGui.QIcon(self.base.get_resource_path("images/icons/data-transfer-upload-3x.png"))
        )
        self.push_button.setStyleSheet(self.base.css["menu_button"])
        self.push_button.clicked.connect(self.push_button_clicked)

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
        self.sync_button.clicked.connect(self.sync_button_clicked)

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
        self.rebase_button.clicked.connect(self.rebase_button_clicked)

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
        self.onion_button.clicked.connect(self.onion_button_clicked)

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
        self.settings_button.clicked.connect(self.settings_button_clicked)

        # Define project status box
        self.project_status_label = QtWidgets.QLabel("{}: ".format(strings._('project_status_label', True)))
        self.project_status_label.setFixedHeight(50)
        self.project_status_label.setStyleSheet(
            self.base.css["project_status_indicator_label"]
        )

        # Define log box
        self.lektor_log_container = QtWidgets.QPlainTextEdit("...")
        self.lektor_log_container.setReadOnly(True)
        self.lektor_log_container.setStyleSheet(
            self.base.css["log_container"]
        )

        self.update_lektor_logs = QtCore.QTimer()
        self.update_lektor_logs.setInterval(50)
        self.update_lektor_logs.start(50)

        # Define tab buttons
        self.lektor_log_button = QtWidgets.QPushButton(strings._('tab_web', True))
        self.lektor_log_button.setFixedHeight(20)
        self.lektor_log_button.setStyleSheet(self.base.css["tab_button"])
        self.lektor_log_button.clicked.connect(self.lektor_log_button_clicked)

        self.git_log_button = QtWidgets.QPushButton(strings._('tab_git', True))
        self.git_log_button.setFixedHeight(20)
        self.git_log_button.setStyleSheet(self.base.css["tab_button"])
        self.git_log_button.clicked.connect(self.git_log_button_clicked)

        self.onion_log_button = QtWidgets.QPushButton(strings._('tab_onion', True))
        self.onion_log_button.setFixedHeight(20)
        self.onion_log_button.setStyleSheet(self.base.css["tab_button"])
        self.onion_log_button.clicked.connect(self.onion_log_button_clicked)

        # Define menu panel
        labels_layout = QtWidgets.QHBoxLayout()
        labels_layout.setSpacing(0)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout = QtWidgets.QHBoxLayout()
        panel_layout.setSpacing(0)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        project_layout = QtWidgets.QHBoxLayout()
        project_layout.setSpacing(0)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        log_layout = QtWidgets.QHBoxLayout()
        log_layout.setSpacing(0)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.setSpacing(0)
        labels_layout.setContentsMargins(0, 0, 0, 0)

        # Add labels to panel
        labels_layout.addWidget(self.open_label)
        labels_layout.addWidget(self.close_label)
        labels_layout.addWidget(self.view_label)
        labels_layout.addWidget(self.edit_label)
        labels_layout.addWidget(self.push_label)
        labels_layout.addWidget(self.sync_label)
        labels_layout.addWidget(self.rebase_label)
        labels_layout.addWidget(self.onion_label)
        labels_layout.addWidget(self.settings_label)

        # Add buttons to panel
        panel_layout.addWidget(self.open_button)
        panel_layout.addWidget(self.close_button)
        panel_layout.addWidget(self.view_button)
        panel_layout.addWidget(self.edit_button)
        panel_layout.addWidget(self.push_button)
        panel_layout.addWidget(self.sync_button)
        panel_layout.addWidget(self.rebase_button)
        panel_layout.addWidget(self.onion_button)
        panel_layout.addWidget(self.settings_button)

        # Add project status to panel
        project_layout.addWidget(self.project_status_label)

        # Add log container to panel
        log_layout.addWidget(self.lektor_log_container)

        # Add tab layout to panel
        tab_layout.addWidget(self.lektor_log_button)
        tab_layout.addWidget(self.git_log_button)
        tab_layout.addWidget(self.onion_log_button)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add panel to layout
        layout.addLayout(labels_layout)
        layout.addLayout(panel_layout)
        layout.addLayout(project_layout)
        layout.addLayout(log_layout)
        layout.addLayout(tab_layout)

        # Create widget
        central_widget = QtWidgets.QWidget()

        # Add layout
        central_widget.setLayout(layout)
        central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

        self.show()

    def open_button_clicked(self):
        self.base.log('GhostWriterGui', 'open_button_clicked')
        self.project = Project(self.base)
        self.open_project = OpenProject(self.base, self.project, self)

        self.lektor_log_container.setPlainText("{}: {}".format(strings._("open_project", True), self.project.folder))

        self.web = Web(self.base, self.project, False)
        self.web.start()

        self.update_lektor_logs.timeout.connect(self.update_web_logs)

    def close_button_clicked(self):
        self.base.log('GhostWriterGui', 'close_button_clicked')

    def view_button_clicked(self):
        self.base.log('GhostWriterGui', 'view_button_clicked')

    def edit_button_clicked(self):
        self.base.log('GhostWriterGui', 'edit_button_clicked')

    def push_button_clicked(self):
        self.base.log('GhostWriterGui', 'push_button_clicked')

    def sync_button_clicked(self):
        self.base.log('GhostWriterGui', 'sync_button_clicked')

    def rebase_button_clicked(self):
        self.base.log('GhostWriterGui', 'rebase_button_clicked')

    def onion_button_clicked(self):
        self.base.log('GhostWriterGui', 'onion_button_clicked')

    def settings_button_clicked(self):
        self.base.log('GhostWriterGui', 'settings_button_clicked')

    def lektor_log_button_clicked(self):
        self.base.log('GhostWriterGui', 'lektor_log_button_clicked')

    def git_log_button_clicked(self):
        self.base.log('GhostWriterGui', 'git_log_button_clicked')

    def onion_log_button_clicked(self):
        self.base.log('GhostWriterGui', 'onion_log_button_clicked')

    def update_web_logs(self):
        self.lektor_log_container.appendPlainText(self.web.check_output().decode('utf-8'))
