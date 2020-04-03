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
import platform

from ghostwriter.settings import Settings
from ghostwriter import strings, base

from PyQt5 import QtCore, QtWidgets, QtGui

class SettingsPanel(QtWidgets.QDialog):
    """
    Settings panel.
    """
    settings_saved = QtCore.pyqtSignal()

    def __init__(self, base, qtapp, layout, config=False):
        super(SettingsPanel, self).__init__()

        self.base = base
        self.qtapp = qtapp
        self.layout = layout
        self.config = config

        self.old_settings = Settings(self.base, self.config)
        self.old_settings.load()

        self.base.log('[GhostWriterGui][SettingsPanel]', '__init__')

        self.setModal(True)
        self.setWindowTitle(strings._("gui_settings_window_title"))
        self.setWindowIcon(
          QtGui.QIcon(self.base.get_resource_path("images/ghostwriter.png"))
        )

        self.system = platform.system()

        self.top_label = QtWidgets.QLabel()
        self.top_label.setPixmap(
          QtGui.QPixmap(self.base.get_resource_path("images/ghostwriter.png"))
        )

        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_layout.addWidget(self.top_label)

        self.upstream_git_repository_label = QtWidgets.QLabel(strings._('upstream_git_repository_label', True))
        self.upstream_git_repository_label.setStyleSheet(self.base.css["settings_label"])
        self.upstream_git_repository_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.upstream_git_repository_field = QtWidgets.QLineEdit(
          self.old_settings.get(
            "upstream_git_repository"
          )
        );

        self.upstream_git_layout = QtWidgets.QHBoxLayout()
        self.upstream_git_layout.setSpacing(0)
        self.upstream_git_layout.setContentsMargins(0, 0, 0, 0)

        self.upstream_git_layout.addWidget(self.upstream_git_repository_label)
        self.upstream_git_layout.addWidget(self.upstream_git_repository_field)

        self.git_repository_label = QtWidgets.QLabel(strings._('git_repository_label', True))
        self.git_repository_label.setStyleSheet(self.base.css["settings_label"])
        self.git_repository_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.git_repository_field = QtWidgets.QLineEdit(
          self.old_settings.get(
            "git_repository"
          )
        );

        self.git_layout = QtWidgets.QHBoxLayout()
        self.git_layout.addWidget(self.git_repository_label)
        self.git_layout.addWidget(self.git_repository_field)

        self.onion_method_label = QtWidgets.QLabel(strings._('onion_method_label', True))
        self.onion_method_label.setStyleSheet(self.base.css["settings_label"])
        self.onion_method_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.onion_radio_button = QtWidgets.QRadioButton("OnionShare")
        self.onion_radio_button.share = "OnionShare"
        self.onion_radio_button.toggled.connect(self.radio_clicked)

        self.docker_radio_button = QtWidgets.QRadioButton("Docker Container")
        self.docker_radio_button.share = "Docker"
        self.docker_radio_button.toggled.connect(self.radio_clicked)

        if self.old_settings.get("onion_share_method") == "docker":
          self.docker_radio_button.setChecked(True)
        else:
          self.onion_radio_button.setChecked(True)

        self.radio_layout = QtWidgets.QHBoxLayout()
        self.radio_layout.addWidget(self.onion_method_label)
        self.radio_layout.addWidget(self.onion_radio_button)
        self.radio_layout.addWidget(self.docker_radio_button)

        self.save_button = QtWidgets.QPushButton(strings._('save_button_label', True));
        self.save_button.setFixedHeight(50)
        self.save_button.setStyleSheet(self.base.css["settings_button"])
        self.save_button.clicked.connect(self.save_clicked)

        self.cancel_button = QtWidgets.QPushButton(strings._('cancel_button_label', True));
        self.cancel_button.setFixedHeight(50)
        self.cancel_button.setStyleSheet(self.base.css["settings_button"])
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.cancel_button)

        settings_layout = QtWidgets.QVBoxLayout()
        settings_layout.addLayout(self.top_layout)
        settings_layout.addLayout(self.upstream_git_layout)
        settings_layout.addLayout(self.git_layout)
        settings_layout.addLayout(self.radio_layout)
        settings_layout.addLayout(self.buttons_layout)

        self.setLayout(settings_layout)

    def radio_clicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
          self.base.log('[GhostWriterGui][SettingsPanel]', 'Share method is %s' % (radioButton.share))
          settings = self.settings_from_panel()
          settings.set(
            "onion_share_method", radioButton.share
          )

    def cancel_clicked(self):
        self.base.log('[GhostWriterGui][SettingsPanel]', 'Cancel settings')
        self.close()

    def save_clicked(self):
        self.base.log('[GhostWriterGui][SettingsPanel]', 'Save settings')

        def changed(s1, s2, keys):
          """
          Compare the Settings objects s1 and s2 and return true if any values
          have changed for the given keys.
          """
          for key in keys:
            if s1.get(key) != s2.get(key):
                return True
          return False

        settings = self.settings_from_panel()
        if settings:
          # If language changed, inform user they need to restart OnionShare
          if changed(settings, self.old_settings, ["locale"]):
            # Look up error message in different locale
            new_locale = settings.get("locale")
            if (
                new_locale in strings.translations
                and "settings_language_changed_notice"
                in strings.translations[new_locale]
            ):
                notice = strings.translations[new_locale][
                  "settings_language_changed_notice"
                ]
            else:
                notice = strings._("settings_language_changed_notice")
            Alert(self.base, notice, QtWidgets.QMessageBox.Information)

          # Save the new settings
          settings.save()

        self.settings_saved.emit()
        self.close()

    def settings_from_panel(self):
        self.base.log('[GhostWriterGui][SettingsPanel]', 'Settings from panel')
        settings = Settings(self.base, self.config)

        settings.set(
          "git_repository", self.git_repository_field.text()
        )

        settings.set(
          "upstream_git_repository", self.upstream_git_repository_field.text()
        )

        if self.onion_radio_button.isChecked():
          settings.set(
            "onion_share_method", "onionshare"
          )
        else:
          settings.set(
            "onion_share_method", "docker"
          )

        return settings
