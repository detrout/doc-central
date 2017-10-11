# docinfo.py
# This module implements DocumentationInfo, which is an object that holds information
# about a single document.

# Import all system packages we need
from debian.deb822 import Deb822
from functools import total_ordering
import html
import re
# Import all our own packages


# Constants to select the sorting order for documents
SORT_TITLE = 1
SORT_SECTION = 2
# Default sorting order
SortMethod = [SORT_TITLE]

pat_paragraph = re.compile('^ \.\n', re.MULTILINE)
pat_verbatim = re.compile('((^  +[^ ].*\n)+)', re.MULTILINE)
pat_url = re.compile('((http|ftp)s?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-./]+)')


@total_ordering
class DocumentationInfo:
    def __init__(self, docfile=None):
        '''DocumentationInfo constructor. If a filename is passed assume
        it is a doc-base file and read it.'''

        self.title = "Nameless document"
        self.author = "Unknown author"
        self.section = "Other"
        self.abstract = "Sorry, there is no abstract available."
        self.docs = {}
        if docfile:
            self.package = docfile.split('/')[-1]
            self.parse_info(docfile)

    def __getkey(self, key):
        '''Return the sorting-key used for sorting. Used by __cmp__ to
        simplify our sorting code.'''

        if (key == SORT_SECTION):
            return self.section
        else:
            return self.title

    def __eq__(self, other):
        '''Compare ourself to another DocumentationInfo object using
        the sorting options defined in SortMethod.'''

        for key in SortMethod:
            if self.__getkey(key).lower() != other.__getkey(key).lower():
                return False

        return True

    def __lt__(self, other):
        '''Compare ourself to another DocumentationInfo object using
        the sorting options defined in SortMethod.'''

        for key in SortMethod:
            if self.__getkey(key).lower() < other.__getkey(key).lower():
                return True

        return False

    def _parse_abstract(self, abstract):
        '''This function converts abstract section'''
        abstract = html.escape(abstract)
        abstract = re.sub(pat_paragraph, '<P>', abstract)
        abstract = re.sub(pat_verbatim, '<PRE>\n\g<1></PRE>', abstract)
        abstract = re.sub(pat_url, '<A HREF="\g<1>">\g<1></A>', abstract)
        return abstract

    def parse_info(self, docfile):
        '''This function reads a doc-base registry file. We use the
        sectionedfile object to get the individual sections from the
        file, and rfc822 object to parse them.'''

        with open(docfile, 'rb') as fp:
            part_iter = Deb822.iter_paragraphs(fp)

            header = next(part_iter)
            self.title = header["Title"]
            if "Author" in header:
                self.author = header["Author"]
            if "Abstract" in header:
                self.abstract = self._parse_abstract(header["Abstract"])
            if "Section" in header:
                self.section = header["Section"]

            for part in part_iter:
                if "Format" not in part:
                    continue
                format = part["Format"].lower()
                if "Index" in part:
                    self.docs[format] = part["Index"]
                else:
                    self.docs[format] = part["Files"]
