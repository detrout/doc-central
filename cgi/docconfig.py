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
docbasedirs		= [ "/usr/share/doc-base" ]

# Descriptions for the various documentation settings. These should probably
# also be in some policy document.
SectionDescr		=  {
	"apps"			: "Documents applications available on your system",
	"apps/graphics"		: "Image processing and other graphics programs",
	"apps/math"		: "Mathematics software",
	"apps/net"		: "Network, mail, news and websoftware ",
	"apps/programming"	: "Programming tools",
	"apps/shells"		: "Shells",
	"apps/sound"		: "Audio software",
	"apps/system"		: "System management tools",
	"apps/text"		: "Text processing software",
	"apps/tools"		: "General utilities",
	"apps/viewers"		: "Documentation and graphics viewers",
	"debian"		: "Documentation on the Debian distribution and project",
	"devel"			: "Information for software developers",
	"help"			: "General documentation, FAQs and HOWTOs",
	"text"			: "Document and text formats",
	}


# vim: ts=8 sw=8 ft=python nowrap

