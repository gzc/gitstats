"""
This class represents one change
mode  0: added; 1: modified; 2: deleted
"""


class Change:
    
	def __init__(self, filename, mode, changeDate, linesOfChange):	
		self.filename = filename
		self.mode = mode
		self.changeDate = changeDate
		self.linesOfChange = linesOfChange