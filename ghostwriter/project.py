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

class Project(object):
    """
    A Project is a Lektor project with its configuration.
    """

    def __init__(self, base, master=None, upstream=None, folder=None):
        self.base = base
        self.base.log("[GhostWriter][Project]", "__init__")

        # Git options
        self.master = master
        self.upstream = upstream

        # Lektor options
        self.folder = folder

    def set_master(self, master):
        self.base.log("[GhostWriter][Project]", "set_master", "master={}".format(master))
        self.master = master

    def set_upstream(self, upstream):
        self.base.log("[GhostWriter][Project]", "set_upstream", "upstream={}".format(upstream))
        self.upstream = upstream

    def set_folder(self, folder):
        self.base.log("[GhostWriter][Project]", "set_folder", "folder={}".format(folder))
        self.folder = folder
