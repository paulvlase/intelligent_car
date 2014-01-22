# File: range_sensor.py

import math
from image_map import ImageMap


"""
	Paul v0.0:
	Senzorii de distanta de pe masina.
"""
class RangeSensor(object):
	
	MAX_DISTANCE = 40
	
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
	def draw(self, painter):
	
		x0 = self.robot.realX
		y0 = self.robot.realY
		
		dx = self.x * 40
		dy = self.y * 40
		
		x1 = x0 + dx
		y1 = y0 + dy

		D = 2 * dy - dx
		
		color = QtGui.QColor(0xFF0000)
		painter.fillRect(x0, y0, 1, 1, color)
		
		for x in range(x0 + 1, x1):
			if D > 0:
				y = y + 1
				painter.fillRect(x, y, 1, 1, color)
				D = D + (2 * dy - 2 * dx)
			else:
				painter.fillRect(x, y, 1, 1, colo)
				D = D + (2 * dy)
	
	
	
	"""
		Intoarce distanta pana la primul obiect de care se loveste daca este mai mica ca distanta maxima
	"""
	def getDistance(self, x0, y0):
		return 0
