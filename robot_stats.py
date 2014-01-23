
from PyQt4 import QtCore, QtGui


class RobotStatsWidget(QtGui.QWidget):

	def __init__(self, robot):
		super(RobotStatsWidget, self).__init__(None)
		
		self.robot = robot
		
		self.initStatsWidget()
	
	
	def initStatsWidget(self):
		
		self.lbl1Text = QtGui.QLabel('L motor speed: ', self)
		self.lbl1Value = QtGui.QLabel('0', self)
		self.lbl1Value.setFixedWidth(50)
		self.lbl1Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.lbl2Text = QtGui.QLabel('R motor speed: ', self)
		self.lbl2Value = QtGui.QLabel('0', self)
		self.lbl2Value.setFixedWidth(50)
		self.lbl2Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.lbl3Text = QtGui.QLabel('L sensor distance ', self)
		self.lbl3Value = QtGui.QLabel('0', self)
		self.lbl3Value.setFixedWidth(50)
		self.lbl3Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.lbl4Text = QtGui.QLabel('F sensor distance: ', self)
		self.lbl4Value = QtGui.QLabel('0', self)
		self.lbl4Value.setFixedWidth(50)
		self.lbl4Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.lbl5Text = QtGui.QLabel('R sensor distance: ', self)
		self.lbl5Value = QtGui.QLabel('0', self)
		self.lbl5Value.setFixedWidth(50)
		self.lbl5Value.setAlignment(QtCore.Qt.AlignRight)
		
		self.bt1 = QtGui.QPushButton('Buton mare', self)
		
		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(self.lbl1Text)
		hbox1.addStretch(1)
		hbox1.addWidget(self.lbl1Value)
		
		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(self.lbl2Text)
		hbox2.addStretch(1)
		hbox2.addWidget(self.lbl2Value)
		
		hbox3 = QtGui.QHBoxLayout()
		hbox3.addWidget(self.lbl3Text)
		hbox3.addStretch(1)
		hbox3.addWidget(self.lbl3Value)
		
		hbox4 = QtGui.QHBoxLayout()
		hbox4.addWidget(self.lbl4Text)
		hbox4.addStretch(1)
		hbox4.addWidget(self.lbl4Value)
		
		hbox5 = QtGui.QHBoxLayout()
		hbox5.addWidget(self.lbl5Text)
		hbox5.addStretch(1)
		hbox5.addWidget(self.lbl5Value)
		
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addLayout(hbox4)
		vbox.addLayout(hbox5)
		vbox.addWidget(self.bt1)
		vbox.addStretch(1)
		
		self.setLayout(vbox)
	
	
	def setLeftMotorSpeed(self, speed):
		
		self.lbl1Value.setText(speed)
		self.repaint()
		
	
	def setRightMotorSpeed(self, speed):
		
		self.lbl2Value.setText(speed)
		self.repaint()
	
	
	def setLeftRangeSensorDistance(self, dist):
		
		self.lbl3Value.setText(dist)
		self.repaint()
	
	
	def setFrontRangeSensorDistance(self, dist):
		
		self.lbl4Value.setText(dist)
		self.repaint()
	
	
	def setRightRangeSensorDistance(self, dist):
		
		self.lbl5Value.setText(dist)
		self.repaint()
