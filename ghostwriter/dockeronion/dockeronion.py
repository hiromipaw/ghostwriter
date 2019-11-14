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

class DockerOnion(object):
    """
    The DockerOnion object is where GhostWriter runs docker images
    """

    def __init__(self, base, project, containers_path, is_cli, log_handler):
        self.base = base
        self.containers_path = containers_path
        self.project = project
        self.log_handler = log_handler
        self.base.log("[GhostWriter][Docker]", "__init__", "is_cli={}".format(is_cli))

    def build(self):
        self.build = Popen(["docker", "build", ".", "-t", "website"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker Build", "pid={}".format(self.build.pid))

    def start(self):
        self.build()
        self.docker = Popen(["docker", "run", "--name", "website", "-t", "-d", "website"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker Start", "pid={}".format(self.docker.pid))
        self.run_tor()
        self.run_web_server()
        self.get_onionservice_address()

    def run_tor(self):
        self.tor = Popen(["docker", "exec", "-t", "-d", "--user=root", "website", "tor"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker run Tor", "pid={}".format(self.tor.pid))

    def run_web_server(self):
        self.nginx = Popen(["docker", "exec", "-t", "-d", "-v", "{}:/var/www/html".format(self.project.folder), "--user=root", "website", "nginx"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker run Nginx", "pid={}".format(self.nginx.pid))

    def get_onionservice_address(self):
        self.onion = Popen(["docker", "exec", "-t", "-d", "--user=root", "website", "cat /home/peer/onion_web_service/hostname"], cwd=self.containers_path, start_new_session=True, stdout=self.log_handler, stderr=self.log_handler)
        self.base.log("[GhostWriter][Docker]", "Docker get onion service address", "pid={}".format(self.onion.pid))

    def status(self):
        outs = None
        errs = None

        try:
            outs, errs = self.docker.communicate(timeout=3)
        except Exception as e:
            self.docker.kill()
            outs, errs = self.docker.communicate()

        return outs, errs

    def check_output(self):
        return self.docker.stdout.readline()

    def stop(self):
        self.docker.terminate()
        self.base.log("[GhostWriter][Web]", "Lektor Stop", "return_code={}".format(self.docker.returncode()))
