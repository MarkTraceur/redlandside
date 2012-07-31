"""
Original software copyright 2010 Mark Holmquist and Logan May.

Some recent modifications copyright 2012 Mark Holmquist.

This file is part of redlandside.

redlandside is licensed under the GNU GPLv3 or later, please see the
COPYING file in this directory or http://www.gnu.org/licenses/gpl-3.0.html for
more information.
"""

import os.path
import os

import PyQt4.QtGui
import PyQt4.QtCore

from synhigh import SyntaxHighlighter

class FileObject (object):

    def __init__(self, parent=None):
        self.parent = parent
        self.filename = ""
        self.language = ""
        self.runcomm = ""
        self.buildcomm = ""

    def newfile(self):
        languages = ["C++", "Python", "Prolog",
                    "Lisp", "Whitespace", "LOLCODE"]
        langdiat = 'Choose a Language'
        langdia = 'Which language are you using today?'
        self.language, ok = PyQt4.QtGui.QInputDialog.getItem(self.parent,
                                                             langdiat,
                                                             langdia,
                                                             languages,
                                                             0, False)
        if ok:
            langlabel = "Current Language: " + self.language
            self.parent.textedit.clear()
            self.parent.textedit.setEnabled(True)
            self.parent.enable_controls()
            self.parent.langlabel.setText("Current Language: " + self.language)
            self.runcomm = ""
            self.parent.highlighter = SyntaxHighlighter(self)

    def openfile(self):
        userpath = os.path.expanduser('~')
        self.filename = PyQt4.QtGui.QFileDialog.getOpenFileName(self.parent,
                                                                'Open file...',
                                                                userpath)
        if self.filename == "":
            return
        fileobject = open(self.filename, 'r')
        self.parent.textedit.setText(fileobject.read())
        self.findtype(self.filename.split(".")[-1])
        fileobject.close()
        self.parent.textedit.setEnabled(True)
        self.parent.enable_controls()
        self.parent.langlabel.setText("Current Language: " + self.language)
        self.parent.highlighter = SyntaxHighlighter(self)
        self.parent.textedit.selectAll()
        self.parent.textedit.cut()
        self.parent.textedit.paste()

    def savefile(self, forcedia = False):
        # Take all the text in the editor, put all the text into a file,
        # and change the filename to that.
        if self.filename == "" or forcedia:
            savedia = PyQt4.QtGui.QFileDialog()
            self.filename = savedia.getSaveFileName(self.parent,
                                                    'Save file...',
                                                    os.path.expanduser('~'))
            savedia.close()
        if self.filename == "":
            return
        fileout = open(self.filename, 'w')
        fileout.write(self.parent.textedit.toPlainText())
        fileout.close()
        self.findtype(self.filename.split(".")[-1])

    def saveas(self):
        self.savefile(True)

    def findtype(self, ext):
        if ext == "cpp":
            self.language = "C++"
            self.runcomm = str(self.filename[:-4])
            self.buildcomm = "g++ " + str(self.filename)
            self.buildcomm += " -o " + str(self.filename[:-4])

        elif ext == "py":
            self.language = "Python"
            self.runcomm = "python " + str(self.filename)
            self.buildcomm = ""

        elif ext == "pro":
            self.language = "Prolog"
            self.runcomm = "prolog -s " + str(self.filename)
            self.buildcomm = ""

        elif ext == "lisp":
            self.language = "Lisp"
            self.runcomm = "clisp " + str(self.filename)
            self.buildcomm = ""

        elif ext == "ws":
            self.language = "Whitespace"
            self.runcomm = "python whitespace/interpret.py "
            self.runcomm += str(self.filename)
            self.buildcomm = ""

        elif ext == "LOL":
            self.language = "LOLCODE"
            self.runcomm = "python lol.py -r " + str(self.filename)
            self.buildcomm = ""
    
