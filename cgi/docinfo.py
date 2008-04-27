# docinfo.py
# This module implements DocumentationInfo, which is an object that holds information
# about a single document.

# Import all system packages we need
import sys, os, rfc822, string, re
# Import all our own packages
import sectionedfile

# Constants to select the sorting order for documents
SORT_TITLE	= 1
SORT_SECTION	= 2
# Default sorting order
SortMethod	= [ SORT_TITLE ]

pat_paragraph	= re.compile('^ \.\n', re.MULTILINE)
pat_verbatim	= re.compile('((^  +[^ ].*\n)+)', re.MULTILINE)
pat_url		= re.compile('((http|ftp)s?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-./]+)')

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

	def _html_encode(self, text):
		'''HTML encodes text '''
		text=string.replace(text, '&', '&amp;')
		text=string.replace(text, '<', '&lt;')
		text=string.replace(text, '>', '&gt;')
		return text


	def _parse_abstract(self, abstract):
		'''This function converts abstract section'''
		abstract=self._html_encode(abstract)
		abstract=re.sub(pat_paragraph, '<P>', abstract)
		abstract=re.sub(pat_verbatim, '<PRE>\n\g<1></PRE>', abstract)
		abstract=re.sub(pat_url, '<A HREF="\g<1>">\g<1></A>', abstract)
		return abstract

		
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
			self.abstract=self._parse_abstract(part.getrawheader("Abstract"))
		if part.has_key("Section"):
			self.section=part.getheader("Section")
		
		while dd.unblock():
			part=rfc822.Message(dd,0)
			if not part.has_key("Format"):
				continue
			format=string.lower(part["Format"])
			if part.has_key("Index"):
				self.docs[format]=part["Index"]
			else:
				self.docs[format]=part["Files"]
