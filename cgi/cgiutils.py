# cgiutils.py
# Copyright 2001 Wichert Akkerman <wichert@wiggy.net>
#
# Utility functions to make writing CGI scripts in python easier.

# Import all system packages we need
import os, string, sys, types, cgi, re, Cookie

def printerror(msg, *args):
	"Print a HTML page with an error and exit"

	print '''<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  <title>error</title>
</head>
<body><h1>error</h1>
'''
	if args:
		print "Error: " + msg % args + '\n' 
	else:
		print "Error: " + msg + '\n' 

	print "</body></html>"
	sys.exit(1)


def extractcookies(dict):
	'''Extract all http cookies that the browser passed to use and
	merge them in dict.'''
	if os.environ.has_key("HTTP_COOKIE"):
		c=Cookie.Cookie(os.environ.get("HTTP_COOKIE"))
		for key in c.keys():
			dict[key]=c[key].value

def extractcgiparams(dict):
	'''Extract all CGI parameters that the browser passed to use and
	merge them in dict.'''
	form=cgi.FieldStorage()
	for frm in form.keys():
		if type(form[frm]) is types.ListType:
			dict[frm]=map(lambda x: x.value, form[frm])
		else:
			dict[frm]=form[frm].value

def setcookie(key,value):
	c=Cookie.Cookie()
	c[key]=value
	print c

def scriptname(script):
	'''Return a URI to another script in the same directory.'''
	if os.environ.has_key("SCRIPT_NAME"):
		base=re.sub("[^/]*$", script, os.environ["SCRIPT_NAME"])
	else:
		base=script
	return base

# vim: ts=8 sw=8 ft=python nowrap

