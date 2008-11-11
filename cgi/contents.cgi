#! /usr/bin/python

# Import all system packages we need
import cgi, os, sys, string, re
# Import all our own stuff
import docinfo, docconfig, docutils

def showsection(sect):
	'''Recursively print a tree of all sections'''

	mydepth=docutils.sectiondepth(sect)
	hdr=0

	if len(sect):
		matcher=re.compile(re.escape(sect+"/"), re.IGNORECASE)
	else:
		matcher=re.compile("")

	for subsect in docutils.sections:
		height=(docutils.sectiondepth(subsect)-mydepth)
		if (matcher.match(subsect) and (height==1)):
			if (hdr==0):
				print "<UL>"
				hdr=1
			print '<LI><A HREF="%s">%s</A>' % \
				(docutils.makesectionlink(subsect), docutils.stripsection(subsect, mydepth))
			showsection(subsect)
	if (hdr==1):
		print "</UL>"

# Get our configuration
docutils.extractcookies()
docutils.extractcgiparams()
# Read the list of documents available
docutils.processdirs()

docutils.cleanupsections()

print "Content-Type: text/html\n"

print '''<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Doc-Base section index</title>
</head>
<body bgcolor="#ffffff" text="#000000" link="#0000cc" vlink="#000066"
  alink="#ff0000"><base target="main">
<a href="/dc/main.html">Home</a>
'''

showsection("")

print """
<form action="%s">
<input type="text" name="keyword">
<input type="submit" value="search">
</form>

</body></html>""" % docutils.scriptname("search.cgi");
