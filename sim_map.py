# File: sim_map.py

import math
from PyQt4 import QtCore, QtGui

from image_map import ImageMap
from robot import Robot
from rectangle import Rectangle


"""
	Paul v0.0:
	Harta pe care se deplaseaza robotul
"""
class Map(QtGui.QFrame):
	
	msg2Statusbar = QtCore.pyqtSignal(str)
	changedStatus = QtCore.pyqtSignal(bool)
	
	MapWidth = 1024
	MapHeight = 640
	Speed = 200
	
	def __init__(self, parent):
		super(Map, self).__init__(parent)
	
		self.parent = parent
	
		self.initMap()
	
	
	def initMap(self):
		QtCore.qDebug('sim_map.Map.initMap')
		
		self.timer = QtCore.QBasicTimer()
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
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
	
		self.saveToImage = True
		
		self.robot = Robot(100, 100, 0)
		
		self.mapChanged = False
	
		self.statsWidget = self.robot.getStatsWidget()
		self.setStatsWidget()
	
	def getObjectAt(self, x, y):
		pass
	
	
	def setObjectAt(self, x, y, shape):
		pass
	
	
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
		self.dragXstart = QMouseEvent.x()
		self.dragYstart = QMouseEvent.y()
		
		self.dragObject = Rectangle()
		self.dragObject.updateDrag(self.dragXstart,
				self.dragYstart, self.dragXstart, self.dragYstart)
		
		#TODO
		#print(QMouseEvent.pos())
	
	
	def mouseMoveEvent(self, QMouseEvent):
		self.dragXend = QMouseEvent.x()
		self.dragYend = QMouseEvent.y()
		
		self.dragObject.updateDrag(self.dragXstart,
				self.dragYstart, self.dragXend, self.dragYend)
		
		#TODO
		#print(QMouseEvent.pos())
		self.repaint()
	
	
	def mouseReleaseEvent(self, QMouseEvent):
		self.dragXend = QMouseEvent.x()
		self.dragYend = QMouseEvent.y()
		
		self.dragObject.updateDrag(self.dragXstart, self.dragYstart,
				self.dragXend, self.dragYend)
		
		self.objects.append(self.dragObject)
		self.dragObject = None
		
		self.saveToImage = True
		self.setChanged(True)
		
		#TODO
		#print(QMouseEvent.pos())
		self.repaint()
	
	
	def paintEvent(self, event):
		
		painter = QtGui.QPainter(self)
		rect = self.contentsRect()
		
		color = QtGui.QColor(0xffffff)
		painter.setPen(0xff0000)
		#QtCore.qDebug('[sim_map.Map.paintEvent] %d %d %d %d' % (rect.top(), rect.left(), rect.bottom(), rect.right())) 
		painter.fillRect(0, 0, rect.right(), rect.bottom(), color)
		
		for obj in self.objects:
			obj.draw(painter)
		
		if not self.dragObject is None:
			self.dragObject.draw(painter)
		
		self.robot.draw(painter)
	
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
			if self.saveToImage == True:
				self.saveToImage = False
				pixmap = QtGui.QPixmap.grabWidget(self)
				ImageMap.image = pixmap.toImage()
				ImageMap.image.save("image.jpg")
			
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
	
	
	def setStatsWidget(self):

		self.parent.setStatsWidget(self.statsWidget)