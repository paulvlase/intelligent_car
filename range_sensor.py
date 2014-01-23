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
	def __init__(self, robot, relDist, x, y):
		
		self.relDist = relDist
		self.x = x
		self.y = y
		self.robot = robot
		self.distance = 0
				
	
	"""
		Odata cu rotirea masinii se roteste si senzorul
	"""
	def rotate(self):
		
		cs = math.cos(self.robot.posTheta)
		sn = math.sin(self.robot.posTheta)
		
		px = self.x * cs - self.y * sn
		py = self.x * sn + self.y * cs
		
		return (px, py)
	
	
	"""
		Deseneaza pe harta o linie ce reprezinta distanta senzorului si directia acestuia
	"""
	def draw(self, painter, color):
		
		coord = self.rotate()
	
		x0 = round(self.robot.posX + coord[0] * self.relDist)
		y0 = round(self.robot.posY + coord[1] * self.relDist)
		
		dx = coord[0] * RangeSensor.MAX_DISTANCE
		dy = coord[1] * RangeSensor.MAX_DISTANCE
		
		x1 = round(x0 + dx)
		y1 = round(y0 + dy)
		
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
			#print('range_sensor.RangeSensor.draw x0: ' + str(x0) + ' y0: ' + str(y0) + ' x1: ' + str(x1) + ' y1: ' + str(y1))
			if x0 < 0 or y0 < 0 or x0 >= ImageMap.width() or y0 >= ImageMap.height():
				return
			
			if ImageMap.pixel(x0, y0) != 0xFFFFFFFF:
				return
			
			painter.fillRect(x0, y0, 1, 1, color)
			
			if x0 == x1 and y0 == y1:
				return
		
			e2 = 2 * err
			if e2 > -dy: 
				err = err - dy
				x0 = x0 + sx
			
			if x0 == x1 and y0 == y1:
				painter.fillRect(x0, y0, 1, 1, color)
				self.distance = RangeSensor.MAX_DISTANCE
				return
			
			if e2 <  dx:
				err = err + dx
				y0 = y0 + sy 
	
	
	'''
		Intoarce distanta pana la primul obiect de care se loveste daca este mai mica ca distanta maxima
	'''
	def getDistance(self):
		coord = self.rotate()
	
		x0 = round(self.robot.posX + coord[0] * self.relDist)
		y0 = round(self.robot.posY + coord[1] * self.relDist)
		
		sX0 = x0
		sY0 = y0
		
		dx = coord[0] * RangeSensor.MAX_DISTANCE
		dy = coord[1] * RangeSensor.MAX_DISTANCE
		
		x1 = round(x0 + dx)
		y1 = round(y0 + dy)
		
		#color = QtGui.QColor(0xFF0000)
		
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
		
		px = x0
		py = y0
		
		while True:
			#TODO cleanup
			#print('range_sensor.RangeSensor.draw x0: ' + str(x0) + ' y0: ' + str(y0) + ' x1: ' + str(x1) + ' y1: ' + str(y1))
			#print('%08X' % (ImageMap.image.pixel(x0, y0),))
			#print('%d - %d' % (x0, y0))
			
			if x0 < 0 or y0 < 0 or x0 >= ImageMap.width() or y0 >= ImageMap.height():
				
				d = math.sqrt(math.pow(sX0 - px, 2.0) + math.pow(sY0 - py, 2.0))
				
				if d > 1000:
					print('A: %d - %d' % (px, py))
				return d
			
			if ImageMap.pixel(x0, y0) != 0xFFFFFFFF:
				
				d =  math.sqrt(math.pow(sX0 - x0, 2.0) + math.pow(sY0 - y0, 2.0))
				
				if d > 1000:
					print('B: %d - %d' % (px, py))
				return d
			
			if x0 == x1 and y0 == y1:
				return RangeSensor.MAX_DISTANCE
			
			e2 = 2 * err
			if e2 > -dy: 
				err = err - dy
				px = x0
				x0 = x0 + sx
			
			if x0 == x1 and y0 == y1:
				return RangeSensor.MAX_DISTANCE
			
			if e2 <  dx:
				err = err + dx
				py = y0
				y0 = y0 + sy 
