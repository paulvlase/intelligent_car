
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QFrame):

	def __init__(self, parent):
		super(MainWindow, self).__init__(parent)
	
		self.parent = parent
		
		self.initWindow()
	
	def initWindow(self):
		
		self.bt1 = QtGui.QPushButton('New file map')
		self.bt1.clicked.connect(self.parent.newMap)
		
		self.bt2 = QtGui.QPushButton('Open file map')
		self.bt2.clicked.connect(self.parent.openMap)
		
		self.bt3 = QtGui.QPushButton('Exit')
		self.bt3.clicked.connect(self.parent.exitSim)
		
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.bt1)
		vbox.addWidget(self.bt2)
		vbox.addWidget(self.bt3)
		self.setLayout(vbox)
