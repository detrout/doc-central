#! /usr/bin/python3

# Import all our own stuff
import docinfo
import docconfig
import docutils

print = docutils.Writer()


def get_sortable_title(doc):
    """Return title with a few common words removed.
    """
    title = doc.title.strip().lower()
    for common in ['a ', 'an ', 'the ']:
        title = title.replace(common, '')
    return title


# Get our configuration
docutils.extractcookies()
docutils.extractcgiparams()
# Read the list of documents available
docutils.processdirs()

docinfo.SortMethod = [docinfo.SORT_SECTION, docinfo.SORT_TITLE]
docutils.documents.sort()
docutils.cleanupsections()

Section = docconfig.Options["section"].strip()

print("Content-Type: text/html; charset=UTF-8\n")

print('''<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Doc-base section index</title>
</head>

<body bgcolor="#ffffff" text="#000000" link="#0000cc" vlink="#000066"
  alink="#ff0000">
<h1>Index for section %s</h1>
<base target="_blank">

Below are the available documents matching your selection. If a document is
available in multiple formats you will see a list for formats next to the
title. If you want to look at a different section or perform a keyword search
please use the left frame.
<p>
<table cellpadding=0 cellspacing=0 border=0><tr><td bgcolor="#000066">
<table cellpadding=0 cellspacing=1 border=0>
''' % Section)

filtered_documents = (d for d in docutils.documents if d.section == Section)
for doc in sorted(filtered_documents, key=get_sortable_title):
    print('<tr><td bgcolor="#ffffff">')
    print('<table cellpadding=3 cellspacing=0 border=0>')
    print('<tr><td bgcolor="#eeeeff" align="right" valign="top"><strong>title:</strong></td>'
          '<td bgcolor="#ffffff"><a href="%s">%s</a>&nbsp;<br></td></tr>' % (docutils.makedoclink(doc), doc.title))
    links = docutils.makedoclinks(doc)
    if links != '':
        print('<tr><th bgcolor="#eeeeff" align=right valign=top><strong>formats:</strong></th>'
              '<td bgcolor="#ffffff">%s&nbsp;<br></td></tr>' % links)
    print('<tr><th bgcolor="#eeeeff" align="right" valign="top"><strong>author:</strong></th>'
          '<td bgcolor="#ffffff">%s&nbsp;<br></td></tr>' % doc.author)
    print('<tr><th bgcolor="#eeeeff" align="right" valign="top"><strong>abstract:</strong></th>'
          '<td bgcolor="#ffffff">%s&nbsp;<br></td></tr>' % doc.abstract)
    if docutils.makeextralinks(doc.package):
        print('<tr><th bgcolor="#eeeeff" align="right" valign="top"><strong>see also:</strong></th>'
              '<td bgcolor="#ffffff">%s&nbsp;<br></td></tr>' % docutils.makeextralinks(doc.package))
    print('</table><p>')
    print('</td></tr>')

print('''</table>
</td></tr></table>
</body></html>
''')
