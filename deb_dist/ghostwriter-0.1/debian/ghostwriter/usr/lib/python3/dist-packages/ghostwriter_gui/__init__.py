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

import signal
import sys

from PyQt5 import QtCore, QtWidgets

from ghostwriter import strings

from ghostwriter.base import Base

from .ghostwriter_gui import GhostWriterGui

class Application(QtWidgets.QApplication):
    """
    This is Qt's QApplication class. It has been overridden to support threads
    and the quick keyboard shortcut.
    """
    def __init__(self, common):
        if common.platform == "Linux" or common.platform == "BSD":
            self.setAttribute(QtCore.Qt.AA_X11InitThreads, True)
        QtWidgets.QApplication.__init__(self, sys.argv)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if (
            event.type() == QtCore.QEvent.KeyPress
            and event.key() == QtCore.Qt.Key_Q
            and event.modifiers() == QtCore.Qt.ControlModifier
        ):
            self.quit()
        return False

def main():
    """
    The main() function implements all of the logic that the GUI version of ghostwriter uses.
    """
    base = Base()
    base.define_css()
    config = False

    strings.load_strings(base)
    print(strings._('version_string').format(base.version))

    # Allow Ctrl-C to smoothly quit the program instead of throwing an exception
    # https://stackoverflow.com/questions/42814093/how-to-handle-ctrlc-in-python-app-with-pyqt
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Start the Qt app
    global qtapp
    qtapp = Application(base)

    # Launch the gui
    gui = GhostWriterGui(base, qtapp, config)

    # Clean up when app quits
    def shutdown():
        print("Shutting down")
        gui.stop()

    qtapp.aboutToQuit.connect(shutdown)

    # All done
    sys.exit(qtapp.exec_())


if __name__ == "__main__":
    main()
