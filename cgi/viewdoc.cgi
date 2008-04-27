#!/usr/bin/python

# Import all system packages we need
import cgi, os, sys, string, re
# Import all our own stuff
import docconfig, docutils

# Get our configuration
docutils.extractcgiparams()

Keyword=string.strip(docconfig.Options["keyword"])

Title = "Direct access to '%s'" % Keyword

print "Content-Type: text/html\n"

print '''<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>%s</title>
</head>

<frameset cols="200,*">
  <frame name="contents" src="/cgi-bin/doc-central/contents.cgi" scrolling="auto">
  <frame name="main" src="/cgi-bin/doc-central/search.cgi?keyword=%s" scrolling="auto">
</frameset>

<noframes>
<body bgcolor="#ffffff" text="#000000" link="#0000cc" vlink="#000066"
  alink="#ff0000">
<h1>Direct Document Access</h1>

<p>You are seeing this because you tried to access a document directly.
However, your browser does not support frames, what causes you to not
have the left menu available while viewing the documentation you want.</p>

<p>To see the left menu and be able to browse all the documentation available,
click <a href="/cgi-bin/doc-central/contents.cgi">here</a>. To go on with the
search you specified in order to get to this page, click
<a href="/cgi-bin/doc-central/search.cgi?keyword=%s">here</a>.</p>

<p>Enjoy!</p>

</body>
</noframes>
</html>''' % (Title, Keyword, Keyword)
