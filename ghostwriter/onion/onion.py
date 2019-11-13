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
from subprocess import Popen

import logging
import sys

class Onion:
    """
    The Onion object is where GhostWriter runs onion services locally
    """

    def __init__(self, base, project, is_cli, log_handler):
        self.base = base
        self.log_handler = log_handler
        self.project = project

        self.base.log("[GhostWriter][Onion]", "__init__", "is_cli={}".format(is_cli))

    def start(self):
        self.onion = Popen(["/home/user/onionshare/dev_scripts/onionshare", "--website", "{}/public".format(self.project.folder)], start_new_session=True, stdout=self.log_handler, stderr=self.log_handler)
        self.base.log("[GhostWriter][Onion]", "Onion Start", "pid={}".format(self.onion.pid))

    def status(self):
        outs = None
        errs = None

        try:
            outs, errs = self.onion.communicate(timeout=3)
        except Exception as e:
            self.onion.kill()
            outs, errs = self.onion.communicate()

        return outs, errs

    def check_output(self):
        return self.onion.stdout.readline()

    def stop(self):
        self.onion.terminate()
        self.base.log("[GhostWriter][Web]", "Lektor Stop", "return_code={}".format(self.onion.returncode()))
