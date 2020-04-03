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

class OnionShare:
    """
    The Onion object is where GhostWriter runs onion services locally
    """

    def __init__(self, base, project, is_cli, log_handler):
        self.base = base
        self.log_handler = log_handler
        self.project = project

        self.base.log("[GhostWriter][Onion]", "__init__", "is_cli={}".format(is_cli))

    def start(self):
        self.share = Popen(["onionshare", "--verbose", "--website", "{}/public".format(self.project.folder)], start_new_session=True)
        self.base.log("[GhostWriter][Onion]", "Onion Start", "pid={}".format(self.share.pid))

    def status(self):
        outs = None
        errs = None

        try:
            outs, errs = self.share.communicate(timeout=3)
        except Exception as e:
            self.share.kill()
            outs, errs = self.share.communicate()

        return outs, errs

    def check_output(self):
        return self.share.stdout.readline()

    def stop(self):
        self.share.terminate()
        self.base.log("[GhostWriter][Onion]", "Onion Stop", "return_code={}".format(self.share.returncode()))
