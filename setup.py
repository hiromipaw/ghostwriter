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

import os, sys, platform, tempfile
from distutils.core import setup


def file_list(path):
    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            files.append(os.path.join(path, filename))
    return files


version = open("share/version.txt").read().strip()
description = (
    """GhostWriter lets you edit a website via lektor, a flexible and powerful """
    """static content management system for building complex and beautiful """
    """websites out of flat files — for people who do not want to make a """
    """compromise between a CMS and a static blog engine.  """
    """GhostWriter works by starting a lektor project that you have cloned via """
    """git. If the project is a fork, you can keep up with upstream by easily """
    """rebasing. The project can be started locally and be edited as a CMS. """
    """Finally it also makes your website accessible as a Tor onion """
    """service, by using either OnionShare or a nginx webserver on a Docker """
    """container. The onion setup is completely transparen for the end user, """
    """ that will be able to access it via Tor Browser"""
)
long_description = (
    description
    + "\n\n"
    + (
        """If you want to edit a website with the ease of a CMS and share it as """
        """static pages GhostWriter starts a lektor server locally and include """
        """some git functionalities to transparently upload your changes or """
        """retrieve updates from an upstream repository. GhostWriter also allow """
        """you to share your work via .onion, by using OnionShare or a nginx """
        """webserver running on a Docker container. Everything is always hosted """
        """on your machine, and disappear when you shutdown GhostWriter. """
        """The .onion can be accessed via Tor Browser. """
    )
)
author = "Hiro"
author_email = "hiro@torproject.org"
url = "https://github.com/hiromipaw/ghostwriter"
license = "GPL v3"
keywords = "lektor, website, docker, container, ghostwriter, onionshare, onion, tor, anonymous, web server"
classifiers = [
    "Programming Language :: Python :: 3",
    "Topic :: Communications :: Website",
    "Topic :: Security :: Cryptography",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Intended Audience :: End Users/Desktop",
    "Operating System :: OS Independent",
    "Environment :: Web Environment",
]
data_files = [
    (
        os.path.join(sys.prefix, "share/applications"),
        ["install/org.ghostwriter.GhostWriter.desktop"],
    ),
    (
        os.path.join(sys.prefix, "share/icons/hicolor/scalable/apps"),
        ["install/org.ghostwriter.GhostWriter.svg"],
    ),
    (
        os.path.join(sys.prefix, "share/metainfo"),
        ["install/org.ghostwriter.GhostWriter.appdata.xml"],
    ),
    (os.path.join(sys.prefix, "share/ghostwriter"), file_list("share")),
    (os.path.join(sys.prefix, "share/ghostwriter/containers"), file_list("share/locale")),
    (os.path.join(sys.prefix, "share/ghostwriter/images"), file_list("share/images")),
    (os.path.join(sys.prefix, "share/ghostwriter/locale"), file_list("share/locale")),
]
if not platform.system().endswith("BSD") and platform.system() != "DragonFly":
    data_files.append(
        (
            "/usr/share/nautilus-python/extensions/",
            ["install/scripts/ghostwriter-nautilus.py"],
        )
    )

setup(
    name="ghostwriter",
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url=url,
    license=license,
    keywords=keywords,
    classifiers=classifiers,
    packages=[
        "ghostwriter",
        "ghostwriter.dockeronion",
        "ghostwriter.onionshare",
        "ghostwriter.web",
        "ghostwriter_gui",
    ],
    include_package_data=True,
    scripts=["install/scripts/ghostwriter", "install/scripts/ghostwriter-gui"],
    data_files=data_files,
)
