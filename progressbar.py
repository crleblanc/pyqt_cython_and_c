#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
from pycproject import cprogram #our Cython C extension module

class MyCustomWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)       

        self.progressBar1 = QtGui.QProgressBar(self)
        self.progressBar1.setRange(0,100)
        button1 = QtGui.QPushButton("Start (with GIL)", self)
        layout.addWidget(self.progressBar1)
        layout.addWidget(button1)

        self.progressBar2 = QtGui.QProgressBar(self)
        self.progressBar2.setRange(0,100)
        button2 = QtGui.QPushButton("Start (no GIL)", self)
        layout.addWidget(self.progressBar2)
        layout.addWidget(button2)

        button1.clicked.connect(self.onStart1)
        button2.clicked.connect(self.onStart2)

        self.myLongTask1 = TaskThreadWithGIL()
        self.myLongTask1.notifyProgress.connect(self.onProgress1)

        self.myLongTask2 = TaskThreadNoGIL()
        self.myLongTask2.notifyProgress.connect(self.onProgress2)


    def onStart1(self):
        self.myLongTask1.start()

    def onStart2(self):
        self.myLongTask2.start()

    def onProgress1(self, i):
        self.progressBar1.setValue(i)

    def onProgress2(self, i):
        self.progressBar2.setValue(i)


class TaskThreadWithGIL(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    
    def run(self):
        
        # Run the Cython wrapper function, which can use a Python 'callable'
        # as a callback.  Here we're updating the progress of a progress bar
        def updater(perc):
            self.notifyProgress.emit(perc)

        cprogram.wrapper_with_callback_gil(self.notifyProgress.emit)
        #cwrapper.wrapper_with_callback(updater)

class TaskThreadNoGIL(TaskThreadWithGIL):
    def run(self):
        cprogram.wrapper_with_callback_nogil(self.notifyProgress.emit)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.path)

    pbarwin = MyCustomWidget()
    pbarwin.show()

    sys.exit(app.exec_())

