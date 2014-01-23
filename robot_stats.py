
from PyQt4 import QtCore, QtGui


class RobotStatsWidget(QtGui.QWidget):

	def __init__(self, robot):
		super(RobotStatsWidget, self).__init__(None)
		
		self.robot = robot
		
		self.initStatsWidget()
	
	
	def initStatsWidget(self):
		
		self.lbl1Text = QtGui.QLabel('L motor speed: ', self)
		self.lbl1Value = QtGui.QLabel('0', self)
		self.lbl1Value.setFixedWidth(20)
		self.lbl1Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.lbl2Text = QtGui.QLabel('R motor speed: ', self)
		self.lbl2Value = QtGui.QLabel('0', self)
		self.lbl2Value.setFixedWidth(20)
		self.lbl2Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.bt1 = QtGui.QPushButton('Buton mare', self)
		
		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(self.lbl1Text)
		hbox1.addStretch(1)
		hbox1.addWidget(self.lbl1Value)
		
		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(self.lbl2Text)
		hbox2.addStretch(1)
		hbox2.addWidget(self.lbl2Value)
		
		
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addWidget(self.bt1)
		vbox.addStretch(1)
		
		self.setLayout(vbox)
	
	
	def setLeftMotorSpeed(self, speed):
		
		self.lbl1Value.setText(speed)
		self.repaint()
		
	
	def setRightMotorSpeed(self, speed):
		
		self.lbl2Value.setText(speed)
		self.repaint()