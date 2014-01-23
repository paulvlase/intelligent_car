
from PyQt4 import QtCore, QtGui

from sim_map import Map
from sim_stats import SimStats

class Placeholder(QtGui.QWidget):

	def __init__(self, parent):
		super(Placeholder, self).__init__(parent)
	
		self.hbox = QtGui.QHBoxLayout(self)
		self.hbox.addWidget(QtGui.QWidget(self))
		self.hbox.addWidget(QtGui.QWidget(self))
		self.setLayout(self.hbox)
		
		self.simMap = Map(self)
		
		self.initPlaceholder()
	
	
	def initPlaceholder(self):
		
		self.hbox.insertWidget(0, self.simMap)
		
		self.setLayout(self.hbox)
	
	
	def setStatsWidget(self, statsWidget):
		self.hbox.insertWidget(1, statsWidget)
