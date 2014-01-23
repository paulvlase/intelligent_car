# File: robot.py

import math
from PyQt4 import QtGui

from range_sensor import RangeSensor
from encoder import Encoder


"""
	Paul v0.0:
	Masina robot.
"""
class Robot(object):
	
	"""
		Paul v0.0:
		realX si realY reprezinta coordonatele de pe plansa.
		logicX si logicY sunt coordonatele relativ la pozitia de start a
		robotului; sunt coordonate deduse de robot.
	"""
	def __init__(self, realX, realY, realTheta):
		
		self.w = 10
		self.h = 15
		
		self.leftRangeSensor = RangeSensor(self, -1, 0)
		self.frontRangeSensor = RangeSensor(self, 0, 1)
		self.rightRangeSensor = RangeSensor(self, 1, 0)
		
		self.leftEncoder = Encoder()
		self.rightEncoder = Encoder()
		
		self.realTheta = realTheta
		self.realX = realX
		self.realY = realY
    
		self.logicalTheta = 0
		self.logicalX = 0
		self.logicalY = 0
    
		self.Rw = 9
		self.Tr = 24
		self.D  = 9
		
		self.dT1 = 0
		self.dT2 = 0
		
		self.T1 = 0
		self.T2 = 0
		
		self.counter = 0
	
	
	def move(self):
		
		self.leftEncoder.addTicks(self.dT1)
		self.rightEncoder.addTicks(self.dT2)
		
		print('dT1: ' + str(self.dT1) + ', dT2: ' + str(self.dT2))
		
		b = 9
		
		if (self.dT2 - self.dT1) < 0.00001:
			dRealTheta = 0
			dRealX = self.dT1 * math.cos(self.realTheta)
			dRealY = self.dT1 * math.sin(self.realTheta)
		elif (self.dT2 - self.dT1) > 24:
			dRealTheta = (self.dT2 - self.dT1) / b
			dRealX = 0
			dRealY = 0
		else:
			R = b / 2 * (self.dT2 + self.dT1) / (self.dT2 - self.dT1)
		
			dRealTheta = (self.dT2 - self.dT1) / b
		
			dRealX = R * (math.sin(dRealTheta + self.realTheta) - math.sin(self.realTheta))
			dRealY = R * (math.cos(self.realTheta) - math.cos(dRealTheta + self.realTheta))
		
		#TODO: This is wrong
		#dRealTheta = 2 * math.pi * (self.Rw / self.D) * \
		#		(self.dT1 + self.dT2) / self.Tr
		
		self.realTheta = self.realTheta + dRealTheta
		
		#TODO: This is wrong
		#dRealX = self.Rw * math.cos(self.realTheta) * \
		#		(self.dT1 - self.dT2) * math.pi / self.Tr
		#dRealY = self.Rw * math.sin(self.realTheta) * \
		#		(self.dT1 - self.dT2) * math.pi / self.Tr
	
		print('dRealTheta: ' + str(dRealTheta) + ', dRealX: ' + str(dRealX) + ', dRealY: ' + str(dRealY))
	
		self.realX = self.realX + dRealX
		self.realY = self.realY + dRealY
		
		print('realTheta: ' + str(self.realTheta) + ', realX: ' + str(self.realX) + ', realY: ' + str(self.realY))
		
		self.counter += 1
		if self.counter == 5:
			self.nextStep()
			self.counter = 0
	
	
	def draw(self, painter):
		
		color = QtGui.QColor(0x00CC66)
		painter.setPen(0x000000)
		painter.fillRect(self.realX, self.realX, self.w, self.h, color)
		
		self.leftRangeSensor.draw(painter, QtGui.QColor(0x00FF00))
		self.frontRangeSensor.draw(painter, QtGui.QColor(0xFF0000))
		self.rightRangeSensor.draw(painter, QtGui.QColor(0x0000FF))
	
	
	def nextStep(self):
		
		#self.dT1 = self.dT1 + 1
		#self.dT2 = self.dT2 + 1
	
		self.T1 = 0
		self.T2 = 0
