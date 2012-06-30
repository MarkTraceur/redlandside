"""
Original software copyright 2010 Mark Holmquist and Logan May.

Some recent modifications copyright 2012 Mark Holmquist.

This file is part of redlandside.

redlandside is licensed under the GNU GPLv3 or later, please see the
COPYING file in this directory or http://www.gnu.org/licenses/gpl-3.0.html for
more information.
"""

#!/usr/bin/python

import os.path
import os
import commands
import time

import PyQt4.QtGui
import PyQt4.QtCore

import fileobject
import synhigh

class MainWindow (PyQt4.QtGui.QMainWindow):
    def __init__(self):
        PyQt4.QtGui.QMainWindow.__init__(self)

        # Set the window size when opened, title the window, and set the icon

        self.currentfile = fileobject.FileObject(parent=self)

        self.resize(800,600)
        self.setWindowTitle('rIDE')
        self.setWindowIcon(PyQt4.QtGui.QIcon('icons/ride.png'))

        # Declare the text field widget, and make it the most important,
        # because the Lady of the Lake raised aloft the blade Excalibur from
        # the lake and gave it to the text widget.

        self.textedit = PyQt4.QtGui.QTextEdit()
        self.setCentralWidget(self.textedit)
        self.textedit.setFontFamily("monospace")
        self.textedit.setLineWrapMode(0)
        welcomemsg = 'Welcome to rIDE\n\n'
        welcomemsg += 'Please create a new file or open an existing one.'
        self.textedit.setText(welcomemsg)
        self.textedit.setEnabled(False)
        self.connect(self.textedit,
                     PyQt4.QtCore.SIGNAL('textChanged()'),
                     self.whenchanged)

        self.highlighter = synhigh.SyntaxHighlighter(self.currentfile)

        # Creates an exit button, sets its icon and adds functionality.

        exit = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/exit.png'),
                                   'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, PyQt4.QtCore.SIGNAL('triggered()'),
                     PyQt4.QtCore.SLOT('close()'))

        # Creates a similar shortcut for a new file

        newfile = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/newfile.png'),
                                      'New', self)
        newfile.setShortcut('Ctrl+N')
        newfile.setStatusTip('Create a new file')
        self.connect(newfile, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.currentfile.newfile)

        # Creates a similar shortcut for opening a file

        openfile = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/openfile.png'),
                                       'Open...', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open a file')
        self.connect(openfile, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.currentfile.openfile)

        # Creates a similar shortcut for saving a file

        savefile = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/savefile.png'),
                                       'Save...', self)
        savefile.setShortcut('Ctrl+S')
        savefile.setStatusTip('Create a new file')
        self.connect(savefile, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.currentfile.savefile)

        # Creates a similar shortcut for saving a file, forcing a dialog.

        saveas = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/savefile.png'),
                                     'Save as...', self)
        saveas.setStatusTip('Save the project as a different filename')
        self.connect(saveas, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.currentfile.saveas)

        # Creates a similar shortcut for building a file

        buildicon = PyQt4.QtGui.QIcon('icons/buildonly.png')
        buildonly = PyQt4.QtGui.QAction(buildicon, 'Build (Ctrl-T)', self)
        buildonly.setShortcut('Ctrl+T')
        buildonly.setStatusTip('Build the project')
        self.connect(buildonly, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.onlybuild)

        # Creates the build-and-run shortcut
        bricon = PyQt4.QtGui.QIcon('icons/buildandrun.png')
        buildrun = PyQt4.QtGui.QAction(bricon, 'Build and Run (Ctrl-B)', self)
        buildrun.setShortcut('Ctrl+B')
        buildrun.setStatusTip('Build the project and run it')
        self.connect(buildrun, PyQt4.QtCore.SIGNAL('triggered()'),
                     self.buildandrun)

        # Creates the run shortcut

        runonly = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon('icons/runonly.png'),
                                      'Run (Ctrl-R)', self)
        runonly.setShortcut('Ctrl+R')
        runonly.setStatusTip('Run the latest build')
        self.connect(runonly, PyQt4.QtCore.SIGNAL('triggered()'), self.onlyrun)

        # Creates the copy shortcut

        copy = PyQt4.QtGui.QAction('Copy', self)
        copy.setShortcut('Ctrl+C')
        copy.setStatusTip('Copy the selected text')
        self.connect(copy, PyQt4.QtCore.SIGNAL('triggered()'), self.textedit,
                     PyQt4.QtCore.SLOT('copy()'))

        # Create the cut shortcut

        cut = PyQt4.QtGui.QAction('Cut', self)
        cut.setShortcut('Ctrl+X')
        cut.setStatusTip('Cut the selected text')
        self.connect(cut, PyQt4.QtCore.SIGNAL('triggered()'), self.textedit,
                     PyQt4.QtCore.SLOT('cut()'))

        # Create the paste shortcut

        paste = PyQt4.QtGui.QAction('Paste', self)
        paste.setShortcut('Ctrl+V')
        paste.setStatusTip('Paste text from the clipboard')
        self.connect(paste, PyQt4.QtCore.SIGNAL('triggered()'), self.textedit,
                     PyQt4.QtCore.SLOT('paste()'))

        # Initialize Status bar

        statusbar = self.statusBar()
        self.langlabel = PyQt4.QtGui.QLabel()
        statusbar.addWidget(self.langlabel)

        # Creates the menu bar and the file menu,
        # adding in the appropriate actions

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newfile)
        file.addAction(openfile)
        file.addAction(savefile)
        file.addAction(saveas)
        file.addAction(exit)

        # Creates the edit menu, adding in the appropriate contents

        edit = menubar.addMenu('&Edit')
        edit.addAction(copy)
        edit.addAction(cut)
        edit.addAction(paste)

        # Make a toolbar with all the trimmings

        self.toolbar = self.addToolBar('Buttons')
        self.toolbar.addAction(newfile)
        self.toolbar.addAction(openfile)
        self.toolbar.addAction(savefile)
        self.toolbar.addAction(buildonly)
        self.toolbar.addAction(buildrun)
        self.toolbar.addAction(runonly)
        self.toolbar.addAction(exit)

    def onlybuild(self):
        # Ask if they want to save the file, then do so--otherwise, throw an
        # error and tell them they want "onlyrun"--then save the file, build it
        # with the appropriate command, and display the results.
        saved = True
        if os.path.isfile(self.currentfile.filename):
            test = open(self.currentfile.filename)
            if test.read() != self.textedit.toPlainText():
                saved = False
        else:
            saved = False
        if not saved:
            t = "WARNING: Save the file!"
            msg = "You should save the file before continuing!"
            ok = "OK"
            c = "Cancel"
            needsave = PyQt4.QtGui.QMessageBox.question(self, t, msg, ok, c)
            if needsave == 0:
                self.currentfile.savefile(True)

        br = "Build results"
        if self.currentfile.language not in ["C++"]:
            msg = "This language doesn't need to be built! Just hit 'Run'!"
            PyQt4.QtGui.QMessageBox.about(self, br, msg)
            raise Exception("This is an interpreted language...")
        statz, outz = commands.getstatusoutput(self.currentfile.buildcomm)
        if statz != 0:
            rbc = "xterm -e '" + self.currentfile.buildcomm
            rbc += "; python pause.py'"
            os.system(rbc)
        else:
            PyQt4.QtGui.QMessageBox.about(self, br, "The build succeeded!")

    def buildandrun(self):
        # Ask if they want to save the file, then do so--otherwise, throw an
        # error--then save the file, build it with the appropriate command, and
        # display the results.
        #
        # If the command used to build it exits with an error, we have a
        # problem--make sure it doesn't close to allow review of the errors,
        # but don't try to run the binary.
        #
        # If it makes it through, close the build window and run the program.
        if self.currentfile.language == "C++":
            self.onlybuild()
        self.onlyrun()

    def onlyrun(self):
        # Find the binary created by the IDE. If it doesn't exist, throw an
        # error. Then, run it.
        if self.currentfile.language not in ['C++']:
            saved = True
            if os.path.isfile(self.currentfile.filename):
                test = open(self.currentfile.filename)
                if test.read() != self.textedit.toPlainText():
                    saved = False
            else:
                saved = False
            if not saved:
                t = "WARNING: Save the file!"
                m = "You should save the file before continuing!"
                ok = "OK"
                c = "Cancel"
                needsave = PyQt4.QtGui.QMessageBox.question(self, t, m, ok, c)
                if needsave == 0:
                    self.currentfile.savefile(True)
        rbc = "xterm -e '" + self.currentfile.runcomm + "; python pause.py'"
        os.system(rbc)

    def whenchanged(self):
        self.textedit.setFontFamily("monospace")
        self.currentfile.saved = False
