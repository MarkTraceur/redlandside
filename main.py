#!/usr/bin/env python

"""
Original software copyright 2010 Mark Holmquist and Logan May.

Some recent modifications copyright 2012 Mark Holmquist.

This file is part of redlandside.

redlandside is licensed under the GNU GPLv3 or later, please see the
COPYING file in this directory or http://www.gnu.org/licenses/gpl-3.0.html for
more information.
"""

#!/usr/bin/python

import sys
import PyQt4.QtGui
import maingui

ride = PyQt4.QtGui.QApplication(sys.argv)
ridemain = maingui.MainWindow()
ridemain.show()
sys.exit(ride.exec_())
