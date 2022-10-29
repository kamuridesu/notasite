import os

AUTHOR = 'kamuridesu'
SITENAME = 'Ergo'
SITEURL = 'https://www.kamuridesu.tech'

PATH = 'content'

TIMEZONE = 'America/Fortaleza'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5

THEME = os.path.join("themes", "mnmlist")

STATIC_PATHS = ['images', 'favicon.ico', 'documents']

MARKUP = ('md',)
# Markdown Configuration:
MARKDOWN = {
    'extension_configs': {
		'markdown.extensions.codehilite': {'css_class': 'highlight codehilite code'},
		# 'markdown.extensions.toc' : {},
		'markdown.extensions.extra': {},
		# 'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True