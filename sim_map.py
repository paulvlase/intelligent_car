# File: sim_map.py

import math
from PyQt4 import QtCore, QtGui

from image_map import ImageMap
from robot import Robot
from rectangle import Rectangle
from target import Target
from sim_stats import SimStats


"""
	Paul v0.0:
	Harta pe care se deplaseaza robotul
"""
class Map(QtGui.QFrame):
	
	msg2Statusbar = QtCore.pyqtSignal(str)
	changedStatus = QtCore.pyqtSignal(bool)
	
	MapWidth = 1024
	MapHeight = 640
	Speed = 100
	
	NoAction = 0
	PlaceBlockAction = 1
	PlaceRobotAction = 2
	PlaceTargetAction = 3
	
	
	def __init__(self, parent):
		super(Map, self).__init__(parent)
	
		self.parent = parent
	
		self.initMap()
	
	
	def initMap(self):
		QtCore.qDebug('sim_map.Map.initMap')
		
		self.timer = QtCore.QBasicTimer()
		self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
		
		self.objects = []
		self.setFocusPolicy(QtCore.Qt.StrongFocus)
		self.setFixedSize(Map.MapWidth, Map.MapHeight)
		self.isStarted = False
		self.isPaused = False
		self.clearMap()
		
		self.dragXstart = -1
		self.dragYstart = -1
		self.dragXend = -1
		self.dragYend = -1
		self.dragObject = None
	
		self.mouseActionType = Map.NoAction
		self.saveToImage = True
		
		self.mapChanged = False
		self.robot = None
		self.target = None
		self.vbox = QtGui.QVBoxLayout()
		self.setLayout(self.vbox)
		self.simStats = SimStats(self)
	
	
	def load(self, fname):
		print("[sim_map.Map.load]")
		
		with open(fname) as fp:
			
			fp.readline()
			
			line = fp.readline().strip().split()
			Map.MapWidth = int(line[0])
			Map.MapHeight = int(line[1])
			Map.Speed = int(line[2])
			
			fp.readline()
			
			line = fp.readline().strip()
			nObjects = int(line)
			
			fp.readline()
			
			for i in range(nObjects):
				line = fp.readline().strip().split()
				
				x = int(line[0])
				y = int(line[1])
				w = int(line[2])
				h = int(line[3])
				
				print(line)
				self.objects.append(Rectangle(x, y, w, h))
	
			self.setFixedSize(Map.MapWidth, Map.MapHeight)
			self.repaint()
		
	
	def save(self, fname):
		print("[sim_map.Map.save]")
		
		self.setChanged(False)
		
		with open(fname, 'w') as fp:
			fp.write('# MapWidth MapHeight Speed\n') 
			fp.write(str(Map.MapWidth) + ' ' + str(Map.MapHeight) + ' ' + str(Map.Speed) + '\n')
			
			fp.write('# Number of objects\n')
			fp.write(str(len(self.objects)) + '\n')
			
			fp.write('# x y width height\n')
			for obj in self.objects:
				fp.write(str(obj) + '\n')
	
	
	def start(self):
		QtCore.qDebug('sim_map.Map.start')
		
		if self.isPaused:
			return
		
		self.isStarted = True
		
		self.clearMap()
		
		self.msg2Statusbar.emit(str(0))
		
		
		self.timer.start(Map.Speed, self)
	
	
	def pause(self):
		QtCore.qDebug('sim_map.Map.pause')
		
		if not self.isStarted:
			return
		
		self.isPaused = not self.isPaused
		
		if self.isPaused:
			self.timer.stop()
			self.msg2Statusbar.emit("paused")
			
		else:
			self.timer.start(Map.Speed, self)
			self.msg2Statusbar.emit(str(0))
		
		self.update()
	
	
	def mousePressEvent(self, QMouseEvent):
		
		x = QMouseEvent.x()
		y = QMouseEvent.y()
		
		if self.mouseActionType == Map.NoAction:
			
			self.dragXstart = x
			self.dragYstart = y
		
			self.dragObject = Rectangle()
			self.dragObject.updateDrag(self.dragXstart,
					self.dragYstart, self.dragXstart, self.dragYstart)
		
			self.mouseActionType = Map.PlaceBlockAction
		
			#TODO cleanup
			#print(QMouseEvent.pos())
		
		elif self.mouseActionType == Map.PlaceRobotAction:
			
			self.robot = Robot(x, y, 0)
			self.setStatsWidget()
			
	
	def mouseMoveEvent(self, QMouseEvent):
		x = QMouseEvent.x()
		y = QMouseEvent.y()
		
		if self.mouseActionType == Map.PlaceBlockAction:
			
			self.dragXend = x
			self.dragYend = y
		
			self.dragObject.updateDrag(self.dragXstart,
					self.dragYstart, self.dragXend, self.dragYend)
		
			#TODO cleanup
			#print(QMouseEvent.pos())
			self.repaint()
	
		elif self.mouseActionType == Map.PlaceRobotAction:
			
			ab = x - self.robot.posX
			mb = math.sqrt(math.pow(x - self.robot.posX, 2) + math.pow(y - self.robot.posY, 2))
			if mb == 0:
				newTheta = 0
			else:
				newTheta = math.acos(ab / mb)
				
				if y < self.robot.posY:
					newTheta = math.pi - newTheta + math.pi
				
			print('theta: %f' % newTheta)
			self.robot.setOrientation(newTheta)
			
			if self.target is not None:
				
				# I am computing the angle relative to Ox ax.
				x = self.target.x - self.robot.posX
				y = self.target.y - self.robot.posY
				
				ab = x
				mb = math.sqrt(x * x + y * y)
			
				if mb == 0:
					theta = 0
				else:
					theta = math.acos(ab / mb)
				
				if self.target.y < self.robot.posY:
					theta = math.pi - theta + math.pi
				
				theta = theta - newTheta
				if theta < 0:
					theta = theta + 2 * math.pi
				
				self.robot.setTargetDirection(theta)
			
			self.repaint()
	
		
	def mouseReleaseEvent(self, QMouseEvent):
		
		x = QMouseEvent.x()
		y = QMouseEvent.y()
		
		if self.mouseActionType == Map.PlaceRobotAction:

			self.mouseActionType = Map.NoAction
			
			self.simStats.btPlaceRobot.setEnabled(False)
			
			ab = x - self.robot.posX
			mb = math.sqrt(math.pow(x - self.robot.posX, 2) + math.pow(y - self.robot.posY, 2))
			if mb == 0:
				newTheta = 0
			else:
				newTheta = math.acos(ab / mb)
			
			if y < self.robot.posY:
				newTheta = math.pi - newTheta + math.pi
			
			self.robot.setOrientation(newTheta)
			
			if self.target is not None:
				
				# I am computing the angle relative to Ox ax.
				x = self.target.x - self.robot.posX
				y = self.target.y - self.robot.posY
				
				ab = x
				mb = math.sqrt(x * x + y * y)
			
				if mb == 0:
					theta = 0
				else:
					theta = math.acos(ab / mb)
				
				if self.target.y < self.robot.posY:
					theta = math.pi - theta + math.pi
				
				theta = theta - newTheta
				if theta < 0:
					theta = theta + 2 * math.pi
				
				self.robot.setTargetDirection(theta)
			
			self.repaint()
			
		elif self.mouseActionType == Map.PlaceTargetAction:
			
			self.target = Target(x, y)
			self.mouseActionType = Map.NoAction
			
			self.simStats.btPlaceTarget.setEnabled(False)
			self.simStats.btPlaceRobot.setEnabled(True)
			
			self.repaint()
			
		elif self.mouseActionType == Map.PlaceBlockAction:
			
			self.dragXend = x
			self.dragYend = y
			
			self.dragObject.updateDrag(self.dragXstart, self.dragYstart,
					self.dragXend, self.dragYend)
		
			self.objects.append(self.dragObject)
			self.dragObject = None
		
			self.saveToImage = True
			self.setChanged(True)
		
			self.mouseActionType = Map.NoAction
			#TODO
			#print(QMouseEvent.pos())
			self.repaint()
	
	
	def paintEvent(self, event):
		rect = self.contentsRect()
		
		if self.saveToImage == True:
			
			ImageMap.image = QtGui.QImage(rect.right(), rect.bottom(), QtGui.QImage.Format_RGB32)
			imagePainter = QtGui.QPainter(ImageMap.image)
			
			self.draw(imagePainter)
			
			ImageMap.image.save('image.jpg')
			
			self.saveToImage = False
	
		painter = QtGui.QPainter(self)
		self.draw(painter)
	
	
	def draw(self, painter):
		
		rect = self.contentsRect()
		
		painter.setPen(QtGui.QColor(0xff0000))
		#TODO
		#QtCore.qDebug('[sim_map.Map.paintEvent] %d %d %d %d' % (rect.top(), rect.left(), rect.bottom(), rect.right())) 
		painter.fillRect(0, 0, rect.right(), rect.bottom(), QtGui.QColor(0xffffff))
		
		for obj in self.objects:
			obj.draw(painter)
		
		if not self.dragObject is None:
			self.dragObject.draw(painter)
			
		if self.robot is not None and self.saveToImage != True:
			self.robot.draw(painter)
		
		if self.target is not None and self.saveToImage != True:
			self.target.draw(painter)
	
	
	def keyPressEvent(self, event):
		
		key = event.key()
		
		if key == QtCore.Qt.Key_S:
			self.start()
			return
		
		if not self.isStarted:
			super(Map, self).keyPressEvent(event)
			return
		
		if key == QtCore.Qt.Key_P:
			self.pause()
			return
		
		if self.isPaused:
			return
		
		elif key == QtCore.Qt.Key_Q:
			self.robot.increaseLeftMotorSpeed(10)
		
		elif key == QtCore.Qt.Key_A:
			self.robot.increaseLeftMotorSpeed(-10)
		
		elif key == QtCore.Qt.Key_E:
			self.robot.increaseRightMotorSpeed(10)
		
		elif key == QtCore.Qt.Key_D:
			self.robot.increaseRightMotorSpeed(-10)
		
		else:
			super(Map, self).keyPressEvent(event)
	
	
	def timerEvent(self, event):
		
		if event.timerId() == self.timer.timerId():
			
			if self.robot is not None:
				self.robot.move()
				self.repaint()
		
		else:
			super(Map, self).timerEvent(event)
	
	
	def clearMap(self):
		self.objects = []


	def changed(self):
		return self.mapChanged


	def setChanged(self, mapChanged):
		self.mapChanged = mapChanged
		self.changedStatus.emit(bool(self.mapChanged))
	
	
	def getStatsWidget(self):
		
		widgets = []
		
		widgets.append(self.simStats)
		
		if self.robot is not None:
			widgets.append(self.robot.getStatsWidget())
	
		return widgets
	
	
	def setStatsWidget(self):
		
		widgets = []
		
		widgets.append(self.simStats)
		
		if self.robot is not None:
			widgets.append(self.robot.getStatsWidget())
		
		self.parent.setStatsWidgets(widgets)


	def placeRobot(self):
		self.mouseActionType = Map.PlaceRobotAction
		
		
	def placeTarget(self):
		self.mouseActionType = Map.PlaceTargetAction
