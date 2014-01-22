
"""
	Paul v0.0:
	Reprezinta componente encoder de pe masina. Aceasta masoara distanta parcursa.
"""
class Encoder(object):

	def __init__(self):
		
		self.ticks = 0;
	
	def addTicks(self, dTicks):
		
		self.ticks = self.ticks + dTicks
