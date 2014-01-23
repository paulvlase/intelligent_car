# File: robot.py

import math
from PyQt4 import QtCore, QtGui

from range_sensor import RangeSensor
from robot_stats import RobotStatsWidget
from encoder import Encoder


"""
	Paul v0.0:
	Masina robot.
"""
class Robot():
	
	"""
		Paul v0.0:
		posX si posY reprezinta coordonatele de pe plansa.
		logicX si logicY sunt coordonatele relativ la pozitia de start a
		robotului; sunt coordonate deduse de robot.
	"""
	
	MaxSpeed = 24
	
	def __init__(self, posX, posY, posTheta):
		
		self.w = 10
		self.h = 15
		
		self.leftRangeSensor = RangeSensor(self, 0, 1)
		self.frontRangeSensor = RangeSensor(self, 1, 0)
		self.rightRangeSensor = RangeSensor(self, 0, -1)
		
		self.leftEncoder = Encoder()
		self.rightEncoder = Encoder()
		
		self.heading = 0
		self.posTheta = posTheta
		self.posX = posX
		self.posY = posY
    
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
	
		self.statsWidget = RobotStatsWidget(self)
	
	def move(self):
		
		self.leftEncoder.addTicks(self.dT1)
		self.rightEncoder.addTicks(self.dT2)
		
		#print('dT1: ' + str(self.dT1) + ', dT2: ' + str(self.dT2))
		
		b = 9
		
		if (self.dT2 - self.dT1) < 0.00001:
			dHeading = 0
			dRealX = self.dT1 * math.cos(self.heading)
			dRealY = self.dT1 * math.sin(self.heading)
		elif (self.dT2 - self.dT1) > 24:
			dHeading = (self.dT2 - self.dT1) / b
			dRealX = 0
			dRealY = 0
		else:
			R = b / 2 * (self.dT2 + self.dT1) / (self.dT2 - self.dT1)
		
			dHeading = (self.dT2 - self.dT1) / b
		
			dRealX = R * (math.sin(dHeading + self.heading) - math.sin(self.heading))
			dRealY = R * (math.cos(self.heading) - math.cos(dHeading + self.heading))
		
		#TODO: This is wrong
		dHeading2 = 2 * math.pi * (self.Rw / self.D) * \
				(self.dT1 - self.dT2) / self.Tr

		
		#TODO: This is wrong
		dRealX2 = self.Rw * math.sin(self.heading) * \
				(self.dT1 + self.dT2) * math.pi / self.Tr
		dRealY2 = self.Rw * math.cos(self.heading) * \
				(self.dT1 + self.dT2) * math.pi / self.Tr
	
		#print('dHeading: ' + str(dHeading2) + ', dRealX2: ' + str(dRealX2) + ', dRealY2: ' + str(dRealY2))
		#print('dRealTheta: ' + str(dHeading) + ', dRealX: ' + str(dRealX) + ', dRealY: ' + str(dRealY))
		
		self.posTheta = self.posTheta + dHeading2
		self.heading = self.heading + dHeading2
		self.posX = self.posX + dRealX2
		self.posY = self.posY + dRealY2
		
		print('heading: ' + str(self.heading) + ', posX: ' + str(self.posX) + ', posY: ' + str(self.posY))
		
		self.counter += 1
		if self.counter == 5:
			self.nextStep()
			self.counter = 0
	
	
	def draw(self, painter):
		
		painter.setPen(QtGui.QColor(0xffffff))
		painter.setBrush(QtGui.QColor(0x00CC66))

		#rect = QtCore.QRect(0, 0, self.w, self.h)
		#original = QtGui.QPolygon(rect, True)
		#painter.drawPolygon(original)		
		
		coords = []
		coords.append(QtCore.QPoint(0, 0))
		coords.append(QtCore.QPoint(self.w, 0))
		coords.append(QtCore.QPoint(self.w, self.h))
		coords.append(QtCore.QPoint(0, self.h))
		
		original = QtGui.QPolygon(coords)
		original.translate(-self.w/2, -self.h/2)
		transform = QtGui.QTransform().rotateRadians(self.posTheta)
		#painter.fillRect(self.posX, self.posX, self.w, self.h, QtGui.QColor(0x0ff000))
		rotated = transform.map(original)
		
		#original.translate(self.posX, self.posY)
		rotated.translate(self.posX, self.posY)
		
		#QtCore.qDebug(str(rotated.point(0)))
		#QtCore.qDebug(str(rotated.point(1)))
		#QtCore.qDebug(str(rotated.point(2)))
		#QtCore.qDebug(str(rotated.point(3)))

		#painter.drawPolygon(original)		
		painter.setBrush(QtGui.QColor(0x0066CC))
		painter.drawPolygon(rotated)

		self.leftRangeSensor.draw(painter, QtGui.QColor(0x00FF00))
		self.frontRangeSensor.draw(painter, QtGui.QColor(0xFF0000))
		self.rightRangeSensor.draw(painter, QtGui.QColor(0x0000FF))
	
	
	def nextStep(self):
		
		#self.dT1 = self.dT1 + 1
		#self.dT2 = self.dT2 + 1
	
		self.T1 = 0
		self.T2 = 0

	def increaseLeftMotorSpeed(self, percent):
		speed = self.dT1 + percent / 100 * Robot.MaxSpeed
		if speed > Robot.MaxSpeed:
			speed = Robot.MaxSpeed
			
		self.setLeftMotorSpeed(self, speed)
	
	def increaseRightMotorSpeed(self, percent):
		speed = self.dT2 + percent / 100 * Robot.MaxSpeed
		if speed > Robot.MaxSpeed:
			speed = Robot.MaxSpeed
			
		self.setRightMotorSpeed(self, speed)

	def setLeftMotorSpeed(self, speed):		
		self.dT1 = speed
		self.statsWidget.setLeftMotorSpeed(str(speed))


	def setRightMotorSpeed(self, speed):
		self.dT2 = speed
		self.statsWidget.setRightMotorSpeed(str(speed))
		
	
	def getStatsWidget(self):
		return self.statsWidget