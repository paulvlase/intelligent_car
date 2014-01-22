# File: robot.py

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
		
		self.w = 5
		self.h = 5
		
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
    
		self.Rw = 0
		self.Tr = 12
		self.D  = 5
		
		self.dT1 = 0
		self.dT2 = 0
		
		self.T1 = 0
		self.T2 = 0
		
		self.counter = 0
	
	
	def run(self):
		
		self.leftEncoder.addTicks(self.T1)
		self.rightEncoder.addTicks(self.dT2)
		
		dRealTheta = 2 * math.pi * (Rw / D) * (self.dT1 - self.dT2) / Tr
		
		self.realTheta = self.realTheta + dRealTheta
		
		self.dRealX = self.Rw * math.cos(self.realTheta) * \
			(self.dT1 + self.dT2) * math.pi / self.Tr
		self.dRealY = self.Rw * math.sin(self.realTheta) * \
			(self.dT1 + self.dT2) * math.pi / self.Tr
	
		self.realX = self.realX + self.dRealX
		self.realY = self.realY + self.dRealY
		
		self.counter += 1
		if self.counter == 5:
			self.nextStep()
			self.counter = 0
	
	
	def draw(self, painter):
		
		color = QtGui.QColor(0x00CC66)
		painter.setPen(0x000000)
		painter.fillRect(self.realX, self.realX, self.w, self.h, color)
		
		leftRangeSensor.draw(painter)
		frontRangeSensor.draw(painter)
		rightRangeSensor.draw(painter)
	
	
	def nextStep(self):
		
		self.dT1 = self.dT1 + 0.01
		self.dT2 = self.dT2 + 0.01
	
		self.T1 = 0
		self.T2 = 0
