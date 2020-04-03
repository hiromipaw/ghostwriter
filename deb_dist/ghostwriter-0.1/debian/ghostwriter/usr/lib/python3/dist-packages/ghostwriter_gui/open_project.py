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
from ghostwriter.settings import Settings

import git


class OpenProject():
    """
    Open a lektor project into the GUI
    """

    def __init__(self, base, project, parent, config=False):

        self.base = base
        self.project = project
        self.parent = parent
        self.config = config

        self.current_settings = Settings(self.base, self.config)
        self.current_settings.load()


        project_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent,
            caption=strings._("gui_choose_folder"),
            options=QtWidgets.QFileDialog.ShowDirsOnly,
        )
        self.project.set_folder(project_folder)
        project_status = "{}: {}".format(strings._("project_status_label", True), self.project.folder)
        self.parent.project_layout.set_project_label(project_status)

        if (self.current_settings.get("project_folder") != project_folder):
            settings = Settings(self.base, self.config)

            settings.set(
                "project_folder", project_folder
            )
            settings.save()
            self.current_settings.load()

        try:
            repo = git.Repo(self.project.folder)

        except Exception as e:
            parent.logs_layout.append_git_log_container(e)

        self.current_settings.set(
            "git_repository", repo.remotes.origin.url
        )

        self.project.set_master =  repo.remotes.origin.url

        self.current_settings.set(
            "upstream_git_repository", repo.remotes.upstream.url
        )

        self.project.set_upstream =  repo.remotes.upstream.url

        self.current_settings.save()
