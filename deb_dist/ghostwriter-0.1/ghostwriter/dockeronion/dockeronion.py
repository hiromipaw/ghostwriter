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
import time
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
        self.build_docker = Popen(["docker", "build", ".", "-t", "website"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker Build", "pid={}".format(self.build_docker.pid))
        self.build_docker.wait()

    def start(self):
        # Here we should check that Popen has finished before calling all the other run functions
        self.build()
        self.docker = Popen(["docker", "run", "-v", "{}/public:/var/www/html".format(self.project.folder), "--name", "website", "-t", "-d", "website"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker Start", "pid={}".format(self.docker.pid))
        self.docker.wait()
        self.run_tor()
        self.run_web_server()
        time.sleep(.5000)
        self.get_onionservice_address()

    def run_tor(self):
        self.tor = Popen(["docker", "exec", "-t", "-d", "--user=root", "website", "tor"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker run Tor", "pid={}".format(self.tor.pid))
        self.tor.wait()

    def run_web_server(self):
        self.nginx = Popen(["docker", "exec", "-t", "-d", "--user=root", "website", "nginx"], cwd=self.containers_path, start_new_session=True)
        self.base.log("[GhostWriter][Docker]", "Docker run Nginx", "pid={}".format(self.nginx.pid))
        self.nginx.wait()

    def get_onionservice_address(self):
        self.onion = Popen(["docker", "exec", "-t", "--user=root", "website", "sh -c \'cat onion_web_service/hostname\'"], cwd=self.containers_path, start_new_session=True, stdout=self.log_handler, stderr=self.log_handler)
        self.base.log("[GhostWriter][Docker]", "Docker get onion service address", "pid={}".format(self.onion.pid))
        self.onion.wait()

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
