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

import json
import os
import platform
import locale

try:
    # We only need pwd module in macOS, and it's not available in Windows
    import pwd
except:
    pass

from . import strings


class Settings(object):
    """
    This class stores all of the settings for Ghostwriter
    """

    def __init__(self, base, config=False):
        self.base = base
        self.base.log("[GhostWriter][Settings]", "__init__")

        # If a readable config file was provided, use that instead
        if config:
            if os.path.isfile(config):
                self.filename = config
            else:
                self.base.log(
                    "[GhostWriter][Settings]",
                    "__init__",
                    "Supplied config does not exist or is unreadable. Falling back to default location",
                )
                self.filename = self.build_filename()

        else:
            # Default config
            self.filename = self.build_filename()

        # Dictionary of available languages in this version, mapped to the
        # language name, in that language
        self.available_locales = {
            "en": "English",  # English
        }

        # These are the default settings. They will get overwritten when loading from disk
        self.default_settings = {
            "version": self.base.version,
            "git_repository": "",
            "upstream_git_repository": "",
            "project_folder": "",
            "onion_share_method": "onionshare",
            "locale": None,  # this gets defined in fill_in_defaults()
        }
        self._settings = {}
        self.fill_in_defaults()


    def fill_in_defaults(self):
        """
        If there are any missing settings from self._settings, replace them with
        their default values.
        """
        for key in self.default_settings:
            if key not in self._settings:
                self._settings[key] = self.default_settings[key]

        # Choose the default locale based on the OS preference, and fall-back to English
        if self._settings["locale"] is None:
            language_code, encoding = locale.getdefaultlocale()

            # Default to English
            if not language_code:
                language_code = "en_US"

            if language_code == "pt_PT" and language_code == "pt_BR":
                # Portuguese locales include country code
                default_locale = language_code
            else:
                # All other locales cut off the country code
                default_locale = language_code[:2]

            if default_locale not in self.available_locales:
                default_locale = "en"
            self._settings["locale"] = default_locale


    def build_filename(self):
        """
        Returns the path of the settings file.
        """
        return os.path.join(self.base.build_data_dir(), "ghostwriter.json")


    def load(self):
        """
        Load the settings from file.
        """
        self.base.log("[GhostWriter][Settings]", "load")

        # If the settings file exists, load it
        if os.path.exists(self.filename):
            try:
                self.base.log(
                    "[GhostWriter][Settings]", "load", "Trying to load {}".format(self.filename)
                )
                with open(self.filename, "r") as f:
                    self._settings = json.load(f)
                    self.fill_in_defaults()
            except:
                pass

        # Make sure data_dir exists
        try:
            os.makedirs(self.get("data_dir"), exist_ok=True)
        except:
            pass

    def save(self):
        """
        Save settings to file.
        """
        self.base.log("[GhostWriter][Settings]", "save")
        open(self.filename, "w").write(json.dumps(self._settings, indent=2))
        self.base.log(
            "[GhostWriter][Settings]", "save", "Settings saved in {}".format(self.filename)
        )


    def get(self, key):
        return self._settings[key]


    def set(self, key, val):
        # If typecasting int values fails, fallback to default values
        if key == "control_port_port" or key == "socks_port":
            try:
                val = int(val)
            except:
                if key == "control_port_port":
                    val = self.default_settings["control_port_port"]
                elif key == "socks_port":
                    val = self.default_settings["socks_port"]

        self._settings[key] = val
