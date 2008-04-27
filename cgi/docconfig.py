# docconfig.py
# This is the central location for all configurable settings in Doc-Central

## User configurable defaults

# The preferred viewing order for document formats. This is used to sort
# the list of available formats and determine to which format the
# title-link will point.
FormatOrder		= [ "html", "info", "pdf", "postscript" ]

# Global map for all options, initialized with some defaults.
Options			= {
	"section"	: "",
	"keyword"	: "",
	"depth"		: "1"
	}

## System defaults

# Location of the doc-base registries. 
docbasedirs		= [ "/var/lib/doc-base/documents" ]

# Descriptions for the various documentation settings. These should probably
# also be in some policy document.
SectionDescr		=  {
	"Graphics"		: "Image processing and other graphics programs",
	"Science/Mathematics"	: "Mathematics software",
	"Network"		: "Network, mail, news and websoftware ",
	"Programming"		: "Programming tools",
	"Shells"		: "Shells",
	"Sound"			: "Audio software",
	"System"		: "System management tools",
	"Text"			: "Text processing software",
	"Viewers"		: "Documentation and graphics viewers",
	"Debian"		: "Documentation on the Debian distribution and project",
	"Help"			: "General documentation, FAQs and HOWTOs"
	}
