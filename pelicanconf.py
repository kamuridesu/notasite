import os

AUTHOR = 'kamuridesu'
SITENAME = 'Ergo'
# SITEURL = 'http://kamuridesu.tech'

PATH = 'content'

TIMEZONE = 'America/Fortaleza'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

THEME = os.path.join("themes", "monospace")

STATIC_PATHS = ['images', 'favicon.ico', 'documents']

MARKUP = ('md',)
# Markdown Configuration:
MARKDOWN = {
    'extension_configs': {
	'markdown.extensions.codehilite': {'css_class': 'highlight'},
	'markdown.extensions.toc' : {},
	'markdown.extensions.extra': {},
	'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True