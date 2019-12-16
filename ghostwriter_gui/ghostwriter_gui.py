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

from ghostwriter import strings, base

from ghostwriter.dockeronion import DockerOnion
from ghostwriter.onionshare import OnionShare
from ghostwriter.project import Project
from ghostwriter.web import Web


from .logs_layout import LogsLayout
from .menu_layout import MenuLayout
from .open_project import OpenProject
from .project_layout import ProjectLayout
from .settings_panel import SettingsPanel


from PyQt5 import QtCore, QtWidgets, QtGui

import git
import webbrowser

class GhostWriterGui(QtWidgets.QMainWindow):
    """
    GhostWriterGui is the main window for the GUI that contains all of the
    GUI elements.
    """

    def __init__(self, base, qtapp, config=False):
        super(GhostWriterGui, self).__init__()

        self.qtapp = qtapp
        self.base = base

        self.base.log("[GhostWriterGui]", "__init__")

        # Load settings, if a custom config was passed in
        self.config = config
        if self.config:
            self.base.load_settings(self.config)
        else:
            self.base.load_settings()

        self.setMinimumWidth(820)
        self.setMinimumHeight(660)

        self.setWindowTitle("GhostWriter")
        self.setWindowIcon(
            QtGui.QIcon(self.base.get_resource_path("images/ghostwriter.png"))
        )

        # System tray
        menu = QtWidgets.QMenu()
        self.settings_action = menu.addAction(strings._('gui_settings_window_title', True))
        self.settings_action.triggered.connect(self.open_settings)
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

        # Create layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.menu_layout = MenuLayout(self.base, self.layout, self)
        self.logs_layout = LogsLayout(self.base, self.layout, self)
        self.project_layout = ProjectLayout(self.base, self.layout, self)

        # Create widget
        central_widget = QtWidgets.QWidget()

        # Add layout
        central_widget.setLayout(self.layout)
        central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

        self.show()


    def open_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Open button clicked')
        self.project = Project(self.base)
        self.open_project = OpenProject(self.base, self.project, self, self.config)
        self.start_web()


    def set_project(self, project_folder):
        self.project = Project(self.base)
        self.project.set_folder(project_folder)

        repository = self.base.settings.get("git_repository")
        if repository:
            self.project.set_master = repository

        upstream_repository = self.base.settings.get("upstream_git_repository")
        if upstream_repository:
            self.project.set_upstream = upstream_repository


    def clean_project(self):
        self.project = None

        self.base.settings.set(
            "project_folder", ""
        )
        self.base.settings.set(
            "upstream_git_repository", ""
        )
        self.base.settings.set(
            "git_repository", ""
        )

        self.base.settings.save()
        self.project_layout.set_project_label("")
        self.logs_layout.reset_lektor_log_container("Project closed.")


    def start_web(self):
        project_label = "{} {}".format(strings._("open_project", True), self.project.folder)
        self.logs_layout.reset_lektor_log_container(project_label)
        self.web = Web(self.base, self.project, False, self.logs_layout.lektor_log_container)
        self.web.start()
        self.logs_layout.append_lektor_log_container("{} {}:{}".format(strings._("serve_project", True), self.web.address, self.web.port))


    def close_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Close button clicked')
        self.web.stop()
        self.clean_project()


    def view_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'View button clicked')
        webbrowser.open('http://localhost:5000')


    def edit_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Edit button clicked')
        webbrowser.open('http://localhost:5000/admin/root%2Ben/edit')


    def push_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Push button clicked')
        self.base.settings.load()
        repository = self.base.settings.get("git_repository")
        if repository:
            try:

                repo = git.Repo(self.project.folder)
                index = repo.index
                index.add([repo.working_tree_dir])
                author = Actor("GhostWriter App", "info@ghostwriter.sh")
                committer = Actor("GhostWriter App", "info@ghostwriter.sh")
                # commit by commit message and author and committer
                index.commit("add changes from ghostwriter app", author=author, committer=committer)
                git.remotes.origin.push()
                self.logs_layout.append_git_log_container("Pushed changes to {}".format(repository))
            except Exception as e:
                self.logs_layout.append_git_log_container(e)
        else:
            self.logs_layout.append_git_log_container("Have you setup a git repository for this project?")


    def sync_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Sync button clicked')
        self.base.settings.load()
        repository = self.base.settings.get("git_repository")
        if repository:
            self.logs_layout.append_git_log_container("Syncing repository {} ... ".format(repository))
            try:
                repo = git.Repo(self.project.folder)
                repo.remotes.origin.pull()
                self.logs_layout.append_git_log_container("Pulled changes from {}".format(repository))
            except Exception as e:
                self.logs_layout.append_git_log_container(e)


    def rebase_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Rebase_button_clicked')
        upstream = self.base.settings.get("upstream_git_repository")
        if upstream:
            self.logs_layout.append_git_log_container("Syncing upstream repository {} ... ".format(upstream))
            try:
                repo = git.Repo(self.project.folder)
                repo.remotes.upstream.pull('master')
                self.logs_layout.append_git_log_container("Pulled changes from {}".format(upstream))
            except Exception as e:
                self.logs_layout.append_git_log_container(e)


    def onion_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Onion button clicked')
        self.logs_layout.show_onion_log_container()

        if (self.base.settings.get("onion_share_method") == "docker"):
            self.logs_layout.reset_onion_log_container("{}: {}".format(strings._("onion_starting", True), self.project.folder))
            self.container_path = self.base.get_resource_path('containers/website')
            self.onion = DockerOnion(self.base, self.project, self.container_path, False, self.logs_layout.onion_log_container)
            self.onion.start()
        else:
            self.onion = OnionShare(self.base, self.project, False, self.logs_layout.onion_log_container)
            self.onion.start()


    def settings_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Settings button clicked')
        self.open_settings()


    def open_settings(self):
        self.base.log('[GhostWriterGui]', 'Open settings panel')

        def reload_settings():
            self.base.log('[GhostWriterGui]', 'Settings have changed')

        p = SettingsPanel(self.base, self.qtapp, self.layout, self.config)
        p.settings_saved.connect(reload_settings)
        p.exec_()


    def lektor_log_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Lektor logs button clicked')
        self.logs_layout.show_lektor_log_container()


    def git_log_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Git logs button clicked')
        self.logs_layout.show_git_log_container()


    def onion_log_button_clicked(self):
        self.base.log('[GhostWriterGui]', 'Onion logs button clicked')
        self.logs_layout.show_onion_log_container()


    def stop(self):
        self.web.stop()
        self.onion.stop()
