
from PyQt4 import QtCore, QtGui


class Target(object):

	R = 10

	def __init__(self, 	x, y):

		self.x = x
		self.y = y
	
	
	def draw(self, painter):
		
		painter.setPen(QtGui.QColor(0xffffff))
		painter.setBrush(QtGui.QColor(0x11AA66))

		painter.drawEllipse(self.x, self.y, Target.R, Target.R)
