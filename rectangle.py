#file: rectangle.py

from PyQt4 import QtCore, QtGui


class Rectangle(object):
	
	def __init__(self, x = 0, y = 0, w = 0, h = 0):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
	
	def draw(self, painter):
		
		color = QtGui.QColor(0x66CC66)
		painter.setPen(0x000000)
		painter.fillRect(self.x, self.y, self.w, self.h, color)
	
	
	def updateDrag(self, dragXstart, dragYstart, dragXend, dragYend):
		self.x = min(dragXstart, dragXend)
		self.y = min(dragYstart, dragYend)
		
		self.w = abs(dragXend - dragXstart)
		self.h = abs(dragYend - dragYstart)
	
	
	def __repr__(self):
		return str(self.x) + ' ' + str(self.y) + ' ' + str(self.w) + ' ' +\
				str(self.h)