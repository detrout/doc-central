# docutils.py
# This module contains all kinds of utility functions that can be used
# throughout Doc-Central.

# Import all system packages we need
import os, string, sys, cgi, re
# Import all our own packages
import docinfo, docconfig

# Some globals that are used throughout doc-central
documents		= []
sections		= []

def processdir(dir):
	'''Read all doc-base entries in a directory and update the globals
	documents and sections to reflect this.'''

	try:
		for entry in os.listdir(dir):
			newdoc=docinfo.DocumentationInfo(dir+"/"+entry)
			if not newdoc.section in sections:
				sections.append(newdoc.section)
			documents.append(newdoc)
	except OSError, err:
		if err.errno != 2:
			printerror("failed to open doc-base directory %s: %s", dir, err)


def processdirs(dirs=docconfig.docbasedirs):
	'''Read all doc-base entries in a list of directories. If no list of
	directories is given default to the globally defined list of directories'''

	for dir in dirs:
		processdir(dir)

def cleanupsections():
	'''Clean up the sections global.

	This means that we make sure that all intermediate sections are also
	in the list, and that the list is sorter alphabetically.'''

	for i in range(len(sections)):
		sections[i]=string.capitalize(sections[i])

	for sect in sections:
		lst=string.split(sect,'/')
		subsect=lst[0]
		while len(lst)>1:
			if not subsect in sections:
				sections.append(subsect)
			del lst[0]
			subsect=subsect+"/"+lst[0]

	sections.sort()
			

def sectiondepth(sect):
	'''Calculate the depth of a section. The depth of the top level
	is defined as 0'''

	if (len(sect)):
		return string.count(sect, "/")+1
	else:
		return 0

def stripsection(sect, count=1, start=0):
	"Strip a number of sections from either the front or back of a section-index."

	if start==0:
		for i in range(count):
			sect=sect[string.find(sect,"/")+1:]
	else:
		for i in range(count):
			j=string.rfind(sect,"/")
			if j==-1:
				sect=""
			else:
				sect=sect[0:string.rfind(sect,"/")]
	return sect


def makesectionlink(sect):
	'''Create a URL to the section-index. We assume that the current
	script is already the browser'''

	if os.environ.has_key("SCRIPT_NAME"):
		base=os.environ["SCRIPT_NAME"]
	else:
		base="browse.cgi"
	return base+"?section="+sect


def makedoclink(doc, format=None):
	'''Create a URL to a specific document. If the document is available in
	multiple formats you can specify the format manually, or otherwise we
	will use the first format from the globally defined FormatList that is
	available'''

	if not len(doc.docs):
		return ''
	if not format:	
		for frm in docconfig.FormatOrder:
			if doc.docs.has_key(frm):
				format=frm
				break
	if not format:
		format=doc.docs.keys()[0]
	
	if format == "info":
		m=re.match("/usr(/share)?/info/([^.]+)\.info", doc.docs[format])
		return "/cgi-bin/info2www?(%s)" % m.group(2)
	else:
		return re.sub("/usr(/share)?/doc/", "/doc/", doc.docs[format])


def makedoclinks(doc):
	'''Build a HTML-string with a list of URLs too all available versions
	of a document.'''
	buf=""
	count=0
	for frm in docconfig.FormatOrder:
		if doc.docs.has_key(frm):
			buf=buf + '<A HREF="%s">[%s]</A>' % (makedoclink(doc,frm),frm)
			count=count+1
	if count>1:
		return buf
	else:
		return ""


def extractcookies(prefix="doc-central_"):
	'''Extract all http cookies that the browser passed to use and
	merge them in docconfig.Options.'''
	if os.environ.has_key("HTTP_COOKIE"):
		for cookie in string.split(os.environ.get("HTTP_COOKIE", ''),';'):
			(key,value)=string.split(string.strip(cookie),"=",2)
			m=re.match("%s(.*)", key)
			docconfig.Options[key]=value

def extractcgiparams():
	'''Extract all CGI parameters that the browser passed to use and
	merge them in docconfig.Options.'''
	form=cgi.FieldStorage()
	for frm in form.keys():
		docconfig.Options[frm]=form[frm].value

def scriptname(script):
	'''Return a link to another script in the same directory.'''
	if os.environ.has_key("SCRIPT_NAME"):
		base=os.path.dirname(os.environ["SCRIPT_NAME"])+"/"
	else:
		base=""

	return base+script

def makesectionlink(sect):
	'''Turn a section-name into an URL to the right section-page using
	browse.cgi'''

	return scriptname("browse.cgi") + "?section=%s" % sect

# vim: ts=8 sw=8 ft=python nowrap

