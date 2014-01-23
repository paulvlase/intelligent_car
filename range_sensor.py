# File: range_sensor.py

from PyQt4 import QtGui

import math
from image_map import ImageMap


"""
	Paul v0.0:
	Senzorii de distanta de pe masina.
"""
class RangeSensor(object):
	
	MAX_DISTANCE = 100
	
	"""
		Paul v0.0:
		x si y sunt din vectorul unitar (x, y).
	"""
	def __init__(self, robot, x, y):
		
		self.x = x
		self.y = y
		self.robot = robot
				
	
	"""
		Odata cu rotirea masinii se roteste si senzorul
	"""
	def rotate(self, theta):
		cs = math.cos(theta)
		sn = math.sin(theta)
		
		px = self.x * cs - self.y * sn
		py = self.x * sn + self.y * cs
		
		self.x = px
		self.y = py
	
	
	"""
		Deseneaza pe harta o linie ce reprezinta distanta senzorului si directia acestuia
	"""
	def draw(self, painter, color):
	
		x0 = self.robot.realX
		y0 = self.robot.realY
		
		dx = self.x * RangeSensor.MAX_DISTANCE
		dy = self.y * RangeSensor.MAX_DISTANCE
		
		x1 = x0 + dx
		y1 = y0 + dy
		
		#color = QtGui.QColor(0xFF0000)
		painter.fillRect(x0, y0, 1, 1, color)
		
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		
		if x0 < x1:
			sx = 1
		else:
			sx = -1
		if y0 < y1:
			sy = 1
		else:
			sy = -1
		err = dx - dy
		
		while True:
			painter.fillRect(x0, y0, 1, 1, color)
			if x0 == x1 and y0 == y1:
				return
		
			e2 = 2 * err
			if e2 > -dy: 
				err = err - dy
				x0 = x0 + sx
			
			if x0 == x1 and y0 == y1:
				painter.fillRect(x0, y0, 1, 1, color)
				return
			
			if e2 <  dx:
				err = err + dx
				y0 = y0 + sy 
	
	
	"""
		Intoarce distanta pana la primul obiect de care se loveste daca este mai mica ca distanta maxima
	"""
	def getDistance(self, x0, y0):
		return 0
