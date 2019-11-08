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

import subprocess

class Web:
    """
    The Web object is where GhostWriter runs lektor locally
    """

    def __init__(self, base, project, is_cli):
        self.base = base
        self.project = project
        self.lektor = None
        self.base.log("[GhostWriter][Web]", "__init__", "is_cli={}".format(is_cli))

    def start(self):
        self.lektor = subprocess.Popen(["lektor", "s"], cwd=self.project.folder, start_new_session=True)
        self.base.log("[GhostWriter][Web]", "Lektor Start", "pid={}".format(self.lektor.pid))

    def status(self):
        outs = None
        errs = None

        try:
            outs, errs = self.lektor.communicate(timeout=15)
        except TimeoutExpired:
            lektor.kill()
            outs, errs = self.lektor.communicate()

        return outs, errs

    def stop(self):
        self.lektor.terminate()
        self.base.log("[GhostWriter][Web]", "Lektor Stop", "return_code={}".format(self.lektor.returncode()))
