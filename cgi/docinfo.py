# docinfo.py
# This module implements DocumentationInfo, which is an object that holds information
# about a single document.

# Import all system packages we need
import sys, os, rfc822, string
# Import all our own packages
import sectionedfile

# Constants to select the sorting order for documents
SORT_TITLE	= 1
SORT_SECTION	= 2
# Default sorting order
SortMethod	= [ SORT_TITLE ]

class DocumentationInfo:
	def __init__(self,docfile=None):
		'''DocumentationInfo constructor. If a filename is passed assume
		it is a doc-base file and read it.'''

		self.title="Nameless document"
		self.author="Unknown author"
		self.section="Other"
		self.abstract="Sorry, there is no abstract available."
		self.docs={}
		if docfile:
			self.package=docfile.split('/')[-1]
			self.parse_info(docfile)

	def __getkey(self,key):
		'''Return the sorting-key used for sorting. Used by __cmp__ to
		simplify our sorting code.'''

		if (key==SORT_SECTION):
			return self.section
		else:
			return self.title

	def __cmp__(self,other):
		'''Compare ourself to another DocumentationInfo object using
		the sorting options defined in SortMethod.'''

		for key in SortMethod:
			(a,b)=(string.lower(self.__getkey(key)), \
				string.lower(other.__getkey(key)))
			if (a<b):
				return -1
			elif (a>b):
				return 1
		return 0
		
	def parse_info(self,docfile):
		'''This function reads a doc-base registry file. We use the 
		sectionedfile object to get the individual sections from the
		file, and rfc822 object to parse them.'''

		fd=os.open(docfile, os.O_RDONLY)
		fo=os.fdopen(fd)
		dd = sectionedfile.SectionedFile(fo)
		dd.divider=""

		part=rfc822.Message(dd,0)
		self.title=part.getheader("Title")
		if part.has_key("Author"):
			self.author=part.getheader("Author")
		if part.has_key("Abstract"):
			self.abstract=part.getheader("Abstract")
		if part.has_key("Section"):
			self.section=string.lower(part.getheader("Section"))
		
		while dd.unblock():
			part=rfc822.Message(dd,0)
			if not part.has_key("Format"):
				continue
			format=string.lower(part["Format"])
			if part.has_key("Index"):
				self.docs[format]=part["Index"]
			else:
				self.docs[format]=part["Files"]
