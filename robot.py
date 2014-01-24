# File: robot.py

import math
from PyQt4 import QtCore, QtGui

from encoder import Encoder
from image_map import ImageMap
from range_sensor import RangeSensor
from robot_stats import RobotStatsWidget


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
		
		self.w = 15
		self.h = 10
		
		self.heading = 0
		self.posTheta = posTheta
		self.posX = posX
		self.posY = posY
    
		self.targetTheta = 0
    
		self.logicalTheta = 0
		self.logicalX = 0
		self.logicalY = 0
    
		self.Rw = 9
		self.Tr = 240
		self.D  = 9
		
		self.dT1 = 0
		self.dT2 = 0
		
		self.T1 = 0
		self.T2 = 0
		
		self.counter = 0
		
		self.leftEncoder = Encoder()
		self.rightEncoder = Encoder()
		
		self.leftRangeSensor = RangeSensor(self, self.h / 2 + 1, 0, -1)
		self.frontRangeSensor = RangeSensor(self, self.w / 2 + 1, 1, 0)
		self.rightRangeSensor = RangeSensor(self, self.h / 2 + 1, 0, 1)
	
		self.statsWidget = RobotStatsWidget(self)
	
	
	def setOrientation(self, posTheta):
		
		self.posTheta = posTheta
		self.statsWidget.setOrientation(self.posTheta)
	
	def setTargetDirection(self, targetTheta):
		
		self.targetTheta = targetTheta
		
		if self.targetTheta > 2 * math.pi:
			self.targetTheta = self.targetTheta % (2 * math.pi)
		elif self.targetTheta < 0:
			self.targetTheta = self.targetTheta % (2 * math.pi)

		#if self.targetTheta > 2 * math.pi:
		#	self.target = 2 * math.pi
		#	print('targetTheta: %f' % self.targetTheta)
		
		#elif self.targetTheta < 0:
		#	self.targetTheta = 0
		#	print('targetTheta: %f' % self.targetTheta)
		
		self.statsWidget.setTargetDirection(self.targetTheta)
	
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
		dRealX2 = self.Rw * math.cos(self.heading) * \
				(self.dT1 + self.dT2) * math.pi / self.Tr
		dRealY2 = self.Rw * math.sin(self.heading) * \
				(self.dT1 + self.dT2) * math.pi / self.Tr
	
		#print('dHeading: ' + str(dHeading2) + ', dRealX2: ' + str(dRealX2) + ', dRealY2: ' + str(dRealY2))
		#print('dRealTheta: ' + str(dHeading) + ', dRealX: ' + str(dRealX) + ', dRealY: ' + str(dRealY))
		
		if self.checkCollision(self.posX + dRealX2, self.posY + dRealY2) == False:
			self.heading = self.heading + dHeading2
			self.posX = self.posX + dRealX2
			self.posY = self.posY + dRealY2
		
			self.setOrientation(self.posTheta)
			self.setTargetDirection(self.targetTheta - dHeading2)
		
		#print('heading: ' + str(self.heading) + ', posX: ' + str(self.posX) + ', posY: ' + str(self.posY))
		
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
		
		leftDist = self.leftRangeSensor.getDistance()
		frontDist = self.frontRangeSensor.getDistance()
		rightDist = self.rightRangeSensor.getDistance()

		self.statsWidget.setLeftRangeSensorDistance(leftDist)
		self.statsWidget.setFrontRangeSensorDistance(frontDist)
		self.statsWidget.setRightRangeSensorDistance(rightDist)
		
		
		dHeading2 = 2 * math.pi * (self.Rw / self.D) * \
				(self.dT1 - self.dT2) / self.Tr
		# dT = dT1 - dT2
		dT = self.targetTheta * self.D * self.Tr / (2 * math.pi * self.Rw)
		
		if dT < 5:
			self.setLeftMotorSpeed(24)
			self.setRightMotorSpeed(24)
		else:
			self.setLeftMotorSpeed(dT)
			self.setRightMotorSpeed(-dT)
		
		self.T1 = 0
		self.T2 = 0
	
	
	def increaseLeftMotorSpeed(self, percent):
		speed = self.dT1 + (percent / 100.0) * Robot.MaxSpeed
		#print('speed: %f, dT1: %f, percent: %f, MaxSpeed: %f' % (speed, self.dT1, percent, Robot.MaxSpeed))
		
		self.setLeftMotorSpeed(speed)
	
	
	def increaseRightMotorSpeed(self, percent):
		speed = self.dT2 + (percent / 100.0) * Robot.MaxSpeed
		#print('speed: %f, dT2: %f, percent: %f, MaxSpeed: %f' % (speed, self.dT2, percent, Robot.MaxSpeed))
		
		self.setRightMotorSpeed(speed)
	
	
	def setLeftMotorSpeed(self, speed):
		self.dT1 = speed
		
		if speed < - Robot.MaxSpeed:
			speed = - Robot.MaxSpeed
		elif speed > Robot.MaxSpeed:
			speed = Robot.MaxSpeed
		
		self.statsWidget.setLeftMotorSpeed(speed)
		#print('dT1: %f dT2: %f' % (self.dT1, self.dT2))
	
	
	def setRightMotorSpeed(self, speed):
		self.dT2 = speed
		
		if speed < - Robot.MaxSpeed:
			speed = - Robot.MaxSpeed
		elif speed > Robot.MaxSpeed:
			speed = Robot.MaxSpeed
		
		self.statsWidget.setRightMotorSpeed(speed)
		#print('dT1: %f dT2: %f' % (self.dT1, self.dT2)) 
	
	
	'''
		O verificare de coliziune rudimentara
	'''
	def checkCollision(self, newPosX, newPosY):
		r = max(self.w, self.h) / 2
		
		x1 = newPosX - r - 1
		y1 = newPosY - r - 1
		x2 = newPosX + r + 1
		y2 = newPosX + r + 1
		
		if x1 < 0 or y1 < 0 or\
			x2 >= ImageMap.image.width() or\
			y2 >= ImageMap.image.height():
			return True
	
		if ImageMap.image.pixel(x1, y1) != 0xFFFFFFFF:
			return True
		if ImageMap.image.pixel(x1, y2) != 0xFFFFFFFF:
			return True
		if ImageMap.image.pixel(x2, y1) != 0xFFFFFFFF:
			return True
		if ImageMap.image.pixel(x2, y2) != 0xFFFFFFFF:
			return True
	
		return False
	
	
	def getStatsWidget(self):
		return self.statsWidget