# File: image_map

"""
	Paul v0.0:
	Retin in asta harta ca o imagine pentru a putea fi calcula distanta pentru senzori.
	Sunt prea prost si am generat un ciclu de importuri.
"""
class ImageMap(object):
	
	image = None
	
	@staticmethod
	def pixel(x, y):
		if ImageMap.image is None:
			return 0
		
		return ImageMap.image.pixel(x, y)
	
	@staticmethod
	def width():
		return ImageMap.image.width()
	
	@staticmethod
	def height():
		return ImageMap.image.height()
