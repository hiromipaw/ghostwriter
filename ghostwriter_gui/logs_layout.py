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

from .logs_handler import QPlainTextEditLogger

from PyQt5 import QtCore, QtWidgets, QtGui

class LogsLayout():
    """
    Add a logs layout into the GUI
    """

    def __init__(self, base, layout, main_window):
        self.base = base
        self.layout = layout
        self.main_window = main_window

        self.log_layout = QtWidgets.QHBoxLayout()
        self.log_layout.setSpacing(0)
        self.log_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout = QtWidgets.QHBoxLayout()
        self.tab_layout.setSpacing(0)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)

        # Define log boxes
        self.lektor_log_container = QPlainTextEditLogger(main_window, self.base)
        self.onion_log_container = QPlainTextEditLogger(main_window, self.base)
        self.git_log_container = QPlainTextEditLogger(main_window, self.base)
        self.lektor_log_container.widget.show()
        self.onion_log_container.widget.hide()
        self.git_log_container.widget.hide()

        # Define tab buttons
        self.lektor_log_button = QtWidgets.QPushButton(strings._('tab_web', True))
        self.lektor_log_button.setFixedHeight(20)
        self.lektor_log_button.setStyleSheet(self.base.css["tab_button"])
        self.lektor_log_button.clicked.connect(main_window.lektor_log_button_clicked)

        self.git_log_button = QtWidgets.QPushButton(strings._('tab_git', True))
        self.git_log_button.setFixedHeight(20)
        self.git_log_button.setStyleSheet(self.base.css["tab_button"])
        self.git_log_button.clicked.connect(main_window.git_log_button_clicked)

        self.onion_log_button = QtWidgets.QPushButton(strings._('tab_onion', True))
        self.onion_log_button.setFixedHeight(20)
        self.onion_log_button.setStyleSheet(self.base.css["tab_button"])
        self.onion_log_button.clicked.connect(main_window.onion_log_button_clicked)

        # Add log container to panel
        self.log_layout.addWidget(self.lektor_log_container.widget)
        self.log_layout.addWidget(self.onion_log_container.widget)
        self.log_layout.addWidget(self.git_log_container.widget)

        # Add tab layout to panel
        self.tab_layout.addWidget(self.lektor_log_button)
        self.tab_layout.addWidget(self.git_log_button)
        self.tab_layout.addWidget(self.onion_log_button)

        # Add panels to layout
        self.layout.addLayout(self.log_layout)
        self.layout.addLayout(self.tab_layout)


    def reset_lektor_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Reset lektor log container')
        self.lektor_log_container.widget.setPlainText(text)


    def append_lektor_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Append lektor log container')
        self.lektor_log_container.widget.appendPlainText(text)


    def reset_onion_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Reset onion log container')
        self.onion_log_container.widget.setPlainText(text)


    def append_onion_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Append onion log container')
        self.onion_log_container.widget.appendPlainText(text)


    def reset_git_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Reset git log container')
        self.git_log_container.widget.setPlainText(text)


    def append_git_log_container(self, text):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Append git log container')
        self.git_log_container.widget.appendPlainText(text)


    def show_onion_log_container(self):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Show onion log container')
        self.lektor_log_container.widget.hide()
        self.git_log_container.widget.hide()
        self.onion_log_container.widget.show()


    def show_git_log_container(self):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Show git log container')
        self.lektor_log_container.widget.hide()
        self.onion_log_container.widget.hide()
        self.git_log_container.widget.show()


    def show_lektor_log_container(self):
        self.base.log('[GhostWriterGui][LogsLayout]', 'Show lektor log container')
        self.lektor_log_container.widget.show()
        self.onion_log_container.widget.hide()
        self.git_log_container.widget.hide()
