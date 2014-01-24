#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: simulator.py

import sys, random
from PyQt4 import QtCore, QtGui


from main_window import MainWindow
from placeholder import Placeholder
from sim_map import Map

"""
	Paul v0.0:
	Fereastra simulatorului.
"""
class Simulator(QtGui.QMainWindow):
	
	def __init__(self):
		super(Simulator, self).__init__()
		
		self.initUI()
	
	
	def initUI(self):
		
		self.fname = QtCore.QString('')
		
		self.placeholder = None
		
		newMapAction = QtGui.QAction(QtGui.QIcon('new.png'), 'New map', self)
		newMapAction.setShortcut('Ctrl+N')
		newMapAction.setStatusTip('New file map')
		newMapAction.triggered.connect(self.newMap)
		
		openMapAction = QtGui.QAction(QtGui.QIcon('open.png'), 'Open map', self)
		openMapAction.setShortcut('Ctrl+O')
		openMapAction.setStatusTip('Open file map')
		openMapAction.triggered.connect(self.openMap)
		
		saveMapAction = QtGui.QAction(QtGui.QIcon('save.png'), 'Save map', self)
		saveMapAction.setShortcut('Ctrl+S')
		saveMapAction.setStatusTip('Save file map')
		saveMapAction.triggered.connect(self.saveMap)
		
		saveAsMapAction = QtGui.QAction(QtGui.QIcon('save.png'), 'Save map as', self)
		saveAsMapAction.setStatusTip('Save file map as')
		saveAsMapAction.triggered.connect(self.saveAsMap)
		
		exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit simulator')
		exitAction.triggered.connect(self.exitSim)
		
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(newMapAction)
		fileMenu.addAction(openMapAction)
		fileMenu.addAction(saveMapAction)
		fileMenu.addAction(saveAsMapAction)
		fileMenu.addAction(exitAction)
		
		#self.statusbar = self.statusBar()        
		#self.simMap.msg2Statusbar[str].connect(self.statusbar.showMessage)
		
		#self.simMap.start()
		self.setCentralWidget(MainWindow(self))

		self.center()
		self.setWindowTitle('Simulator')        
		self.show()
	
	
	def newMap(self):
		
		QtCore.qDebug('simulator.Simulator.newMap')
		
		self.fname = QtCore.QString('')
		self.placeholder = Placeholder(self)
		
		self.setWindowTitle('Untitled - Simulator')
		self.setCentralWidget(self.placeholder)
		self.placeholder.simMap.changedStatus[bool].connect(self.setChanged)
	
	
	def openMap(self):
	
		QtCore.qDebug('simulator.Simulator.openMap')
		
		if self.saveMap(True) == True:
		
			fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file map', '', 'Simulator maps (*.map)')
		
			if fname.length > 0:
				self.fname = fname

				self.placeholder = Placeholder(self)

				self.setWindowTitle(self.fname + ' - Simulator')
				self.setCentralWidget(self.placeholder)
				
				self.placeholder.simMap.load(self.fname)
				self.placeholder.simMap.changedStatus[bool].connect(self.setChanged)
			
			print(self.fname)
	
	
	def saveMap(self, confirmation = False):
	
		QtCore.qDebug('simulator.Simulator.saveMap')
		
		if  (not self.placeholder is None) and (not self.placeholder.simMap is None) and self.placeholder.simMap.changed():
			if self.fname.length() > 0:
		
				msgBox = QtGui.QMessageBox();
				msgBox.setText("The document has been modified.");
				msgBox.setInformativeText("Do you want to save your changes?");
				msgBox.setStandardButtons(QtGui.QMessageBox.Save |
						QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel);
				msgBox.setDefaultButton(QtGui.QMessageBox.Save);
				ret = msgBox.exec_();
				
				if ret == QtGui.QMessageBox.Save:
					self.placeholder.simMap.save(self.fname)
					return True
				elif ret == QtGui.QMessageBox.Discard:
					return True
				else:
					return False

			else:
				fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file map', '', 'Simulator maps (*.map)')
			
				if fname.length() > 0:
					self.fname = fname
					self.setWindowTitle(self.fname)
				
			if self.fname.length() > 0:
				self.placeholder.simMap.save(self.fname)
			
			print(self.fname)
		return True
	
	
	def saveAsMap(self):
		QtCore.qDebug('simulator.Simulator.saveAsMap')
		
		self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file map as', '', 'Simulator maps (*.map)')
		if fname.length() > 0:
			self.fname = fname
			self.placeholder.simMap.save(self.fname)
		
		print(self.fname)
	
	
	def exitSim(self):
		
		QtCore.qDebug('simulator.Simulator.exitMap')
		
		if self.saveMap() == True:
			QtGui.qApp.quit()
	
	
	def setChanged(self, changed):
		fname = self.fname
		if fname.length() == 0:
			fname = QtCore.QString('Untitled')
		
		if changed == True:
			self.setWindowTitle(fname + '*' + '- Simulator')
		else:
			self.setWindowTitle(fname + ' - Simulator')
		
	
	def center(self):
		
		screen = QtGui.QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2, 
			(screen.height() - size.height()) /2)


def main():
	
	app = QtGui.QApplication([])
	simulator = Simulator()    
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
