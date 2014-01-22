	#!/usr/bin/python
	# -*- coding: utf-8 -*-

	# file: simulator.py


	import sys, random
	from PyQt4 import QtCore, QtGui

	import navigation
	from rectangle import Rectangle

	class Simulator(QtGui.QMainWindow):
		
		def __init__(self):
			super(Simulator, self).__init__()
			
			self.initUI()
		
		
		def initUI(self):    
			
			self.tMap = Map(self)
			self.setCentralWidget(self.tMap)
			
			self.statusbar = self.statusBar()        
			self.tMap.msg2Statusbar[str].connect(self.statusbar.showMessage)
			
			self.tMap.start()
			
			self.resize(180, 380)
			self.center()
			self.setWindowTitle('Simulator')        
			self.show()
			
		
		def center(self):
			
			screen = QtGui.QDesktopWidget().screenGeometry()
			size = self.geometry()
			self.move((screen.width()-size.width())/2, 
				(screen.height()-size.height())/2)
		

	class Map(QtGui.QFrame):
		
		msg2Statusbar = QtCore.pyqtSignal(str)
		
		MapWidth = 360
		MapHeight = 180
		Speed = 300
		MapImage = None
		
		
		def __init__(self, parent):
			super(Map, self).__init__(parent)
			
			self.initMap()
		
		
		def initMap(self):
			
			self.timer = QtCore.QBasicTimer()
			
			self.objects = []
			
			self.setFocusPolicy(QtCore.Qt.StrongFocus)
			self.isStarted = False
			self.isPaused = False
			self.clearMap()
			
			self.dragXstart = -1
			self.dragYstart = -1
			self.dragXend = -1
			self.dragYend = -1
			self.dragObject = None
		
			self.saveToImage = true
		
		def getObjectAt(self, x, y):
			pass
		
		
		def setObjectAt(self, x, y, shape):
			pass
		
		
		def start(self):
			
			if self.isPaused:
				return
			
			self.isStarted = True
			
			self.clearMap()
			
			self.msg2Statusbar.emit(str(0))
			
			
			self.timer.start(Map.Speed, self)
		
		
		def pause(self):
			
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
			
			print(QMouseEvent.pos())
		
		
		def mouseMoveEvent(self, QMouseEvent):
			self.dragXend = QMouseEvent.x()
			self.dragYend = QMouseEvent.y()
			
			self.dragObject = Rectangle()
			self.dragObject.updateDrag(self.dragXstart,
					self.dragYstart, self.dragXend, self.dragYend)
			
			print(QMouseEvent.pos())
			self.repaint()
		
		
		def mouseReleaseEvent(self, QMouseEvent):
			self.dragXend = QMouseEvent.x()
			self.dragYend = QMouseEvent.y()
			
			self.dragObject.updateDrag(self.dragXstart, self.dragYstart,
					self.dragXend, self.dragYend)
			
			self.objects.append(self.dragObject)
			self.dragObject = None
			
			self.saveToImage = True
			
			print(QMouseEvent.pos())
			self.repaint()
		
		
		def paintEvent(self, event):
			
			painter = QtGui.QPainter(self)
			rect = self.contentsRect()
			
			MapTop = rect.bottom() - Map.MapHeight
			
			for obj in self.objects:
				obj.draw(painter)
			
			if not self.dragObject is None:
				self.dragObject.draw(painter)
			
			if saveToImage == True:
				pixmap = QtGui.QPixmap.grabWidget(self)
				self.MapImage = pixmap.toImage()
				self.MapImage.save("image.jpg")
			
			print("Paint event fired")
		
		def keyPressEvent(self, event):
			
			if not self.isStarted:
				super(Map, self).keyPressEvent(event)
				return
			
			key = event.key()
			
			if key == QtCore.Qt.Key_P:
				self.pause()
				return
			
			if self.isPaused:
				return
			
			elif key == QtCore.Qt.Key_S:
				pixmap = QtGui.QPixmap.grabWidget(self)
				image = pixmap.toImage()
				image.save("image.jpg")
				
				self.saveToImage = False
			
			else:
				super(Map, self).keyPressEvent(event)
		
		
		def timerEvent(self, event):
			
			if event.timerId() == self.timer.timerId():
				robot.nextStep()
			
			else:
				super(Map, self).timerEvent(event)
		
		
		def clearMap(self):
			self.objects = []


	def main():
		
		app = QtGui.QApplication([])
		simulator = Simulator()    
		sys.exit(app.exec_())


	if __name__ == '__main__':
		main()
