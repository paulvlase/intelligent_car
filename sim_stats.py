
from PyQt4 import QtCore, QtGui

from global_config import GlobalConfig


class SimStats(QtGui.QFrame):
	
	def __init__(self, parent):
		super(SimStats, self).__init__(parent)
		
		self.parent = parent
		
		self.initWidgets()
	
	
	def initWidgets(self):
		
		self.setFixedWidth(GlobalConfig.StatsWidgetWidth)
		
		self.btPlaceTarget = QtGui.QPushButton('Place target')
		self.btPlaceTarget.clicked.connect(self.parent.placeTarget)
		
		self.btPlaceRobot = QtGui.QPushButton('Place robot')
		self.btPlaceRobot.setEnabled(False)
		self.btPlaceRobot.clicked.connect(self.parent.placeRobot)
		
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.btPlaceTarget)
		self.vbox.addWidget(self.btPlaceRobot)
		
		self.setLayout(self.vbox)
		
		self.show()