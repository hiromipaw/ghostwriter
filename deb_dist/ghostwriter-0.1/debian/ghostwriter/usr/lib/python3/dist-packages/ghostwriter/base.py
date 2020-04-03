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
import inspect
import os
import platform
import sys
import time

from .settings import Settings

class Base(object):
    """
    The Base object is shared amongst all parts of Ghostwriter.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

        # The platform GhostWriter is running on
        self.platform = platform.system()
        if self.platform.endswith("BSD") or self.platform == "DragonFly":
            self.platform = "BSD"

        # The current version of GhostWriter
        with open(self.get_resource_path("version.txt")) as f:
            self.version = f.read().strip()


    def log(self, module, func, msg=None):
        """
        If verbose mode is on, log error messages to stdout
        """
        if self.verbose:
            timestamp = time.strftime("%b %d %Y %X")

            final_msg = "[{}] {}.{}".format(timestamp, module, func)
            if msg:
                final_msg = "{}: {}".format(final_msg, msg)
            print(final_msg)


    def load_settings(self, config=None):
        """
        Loading settings, optionally from a custom config json file.
        """
        self.settings = Settings(self, config)
        self.settings.load()


    def get_resource_path(self, filename):
        """
        Returns the absolute path of a resource, regardless of whether GhostWriter is installed
        systemwide, and whether regardless of platform
        """
        # On Windows, and in Windows dev mode, switch slashes in incoming filename to backslackes
        if self.platform == "Windows":
            filename = filename.replace("/", "\\")

        if getattr(sys, "ghostwriter_dev_mode", False):
            # Look for resources directory relative to python file
            prefix = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(inspect.getfile(inspect.currentframe()))
                    )
                ),
                "share",
            )
            if not os.path.exists(prefix):
                # While running tests during stdeb bdist_deb, look 3 directories up for the share folder
                prefix = os.path.join(
                    os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.dirname(prefix)))
                    ),
                    "share",
                )

        elif self.platform == "BSD" or self.platform == "Linux":
            # Assume GhostWriter is installed systemwide in Linux, since we're not running in dev mode
            prefix = os.path.join(sys.prefix, "share/ghostwriter")

        elif getattr(sys, "frozen", False):
            # Check if app is "frozen"
            # https://pythonhosted.org/PyInstaller/#run-time-information
            if self.platform == "Darwin":
                prefix = os.path.join(sys._MEIPASS, "share")
            elif self.platform == "Windows":
                prefix = os.path.join(os.path.dirname(sys.executable), "share")

        return os.path.join(prefix, filename)


    def build_data_dir(self):
        """
        Returns the path of the data directory.
        """
        if self.platform == "Windows":
            try:
                appdata = os.environ["APPDATA"]
                ghostwriter_data_dir = "{}\\GhostWriter".format(appdata)
            except:
                # If for some reason we don't have the 'APPDATA' environment variable
                # (like running tests in Linux while pretending to be in Windows)
                ghostwriter_data_dir = os.path.expanduser("~/.config/ghostwriter")
        elif self.platform == "Darwin":
            ghostwriter_data_dir = os.path.expanduser(
                "~/Library/Application Support/GhostWriter"
            )
        else:
            ghostwriter_data_dir = os.path.expanduser("~/.config/ghostwriter")

        os.makedirs(ghostwriter_data_dir, 0o700, True)
        return ghostwriter_data_dir


    def define_css(self):
        """
        This defines all of the stylesheets used in GUI mode, to avoid repeating code.
        This method is only called in GUI mode.
        """
        self.css = {
            "menu_label": """
                QLabel {
                    color: #4711B8;
                    background-color: #fefefe;
                    border: 0;
                    border-radius: 0;
                }""",
            "menu_button": """
                QPushButton {
                    color: #4711B8;
                    background-color: #fefefe;
                    border: 0;
                    border-radius: 0;
                }""",
            "tab_button": """
                QPushButton {
                    color: #4711B8;
                    background-color: #fefefe;
                    border: 0;
                    border-right: 1px solid #4711B8;
                    border-radius: 0;
                }""",
            "project_status_indicator_label": """
                QLabel {
                    color: #fefefe;
                    background-color: #4711B8;
                    border: 0;
                    border-top: 1px solid #fdfdfd;
                    border-bottom: 1px solid #fdfdfd;
                    border-radius: 0;
                }""",
            "log_container": """
                QPlainTextEdit {
                    color: #fefefe;
                    background-color: #222;
                    border: 0;
                    border-top: 1px solid #fdfdfd;
                    border-bottom: 1px solid #fdfdfd;
                    border-radius: 0;
                }""",
            "settings_label": """
                QLabel {
                    color: #4711B8;
                    border: 0;
                    border-radius: 0;
                }""",
            "settings_button": """
                QLabel {
                    color: #fefefe;
                    background-color: #4711B8;
                    border: 0;
                    border-radius: 0;
                }""",
        }
