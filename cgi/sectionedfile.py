# sectionedfily.py
#
# A sectionedfile is a file that contains multiple sections, which are seperator
# by a specific seperator.

# Import all system packages we need
import sys, string

class SectionedFile:
	def __init__(self, fp):
		'''Simple constructor to initialize our data'''

		self.fp=fp
		self.blocked=0
		self.eof=0
		self.divider=''
		self.mustunget=0
		self.unget=''

	def readline(self):
		'''Read the next line from our input. If we hit a divider we return
		an empty line and block ourselves. Dividers found at the beginning
		are skipped.'''

		if self.blocked:
			return ''
		eating=0
		while 1:
			line=''
			if self.mustunget:
				line=self.unget
				self.mustunget=0
			else:
				line=self.fp.readline()
				if not line:
					self.eof=1
					self.blocked=1
					return ''

			if string.strip(line)==self.divider:
				eating=1
				continue;
			else:
				if eating:
					self.mustunget=1
					self.unget=line
					self.blocked=1
					return ''
				else:
					return line
		self.newblock=0
		return line

	def readlines(self):
		'''Read as much lines from our input as possible until we hit a
		divider.'''

		lines=[]
		while 1:
			line=self.readline()
			if not line:
				break
			lines.append(line)
		return lines

	def read(self):
		'''Read all lines up to a divider and return them.'''

		return string.joinfields(self.readlines(), '')

	def unblock(self):
		'''Unblock ourselves so we can proceed to the next section.'''

		if self.eof:
			return 0
		self.blocked=0
		self.newblock=1
		return 1
