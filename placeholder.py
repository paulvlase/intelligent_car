
from PyQt4 import QtCore, QtGui

from sim_map import Map

class Placeholder(QtGui.QWidget):

	RightWidgetWidth = 175

	def __init__(self, parent):
		super(Placeholder, self).__init__(parent)
		
		self.initPlaceholder()
	
	
	def initPlaceholder(self):
		
		self.simMap = Map(self)
		
		self.hbox = QtGui.QHBoxLayout()
		
		self.vbox = QtGui.QVBoxLayout()
		
		self.hbox.addWidget(self.simMap)
		
		widgets = self.simMap.getStatsWidget()
		
		for widget in widgets:
			self.vbox.addWidget(widget)
		
		self.vbox.addStretch(1)
		
		self.hbox.addLayout(self.vbox)
		
		self.setLayout(self.hbox)

	
	def setStatsWidgets(self, widgets):
		while self.vbox.takeAt(0) is not None:
			self.vbox.removeItem(self.vbox.takeAt(0))

		for widget in widgets:
			self.vbox.addWidget(widget)
		
		self.vbox.addStretch(1)
