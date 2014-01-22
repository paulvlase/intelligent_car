#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: simulator.py

import sys, random
from PyQt4 import QtCore, QtGui

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
		
		self.sMap = Map(self)
		self.setCentralWidget(self.sMap)
		
		self.statusbar = self.statusBar()        
		self.sMap.msg2Statusbar[str].connect(self.statusbar.showMessage)
		
		self.sMap.start()
		
		self.resize(180, 380)
		self.center()
		self.setWindowTitle('Simulator')        
		self.show()
	
	
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
