#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os.path import abspath, join, dirname

AUTHOR = "Balthazar Rouberol"
AUTHOR_TWITTER = "@brouberol"
AUTHOR_URL = "https://balthazar-rouberol.com"
SITENAME = "Balthazar"
SITEURL = "https://blog.balthazar-rouberol.com"
ISSOURL = "https://comments.balthazar-rouberol.com"
ABSOLUTE_SITEURL = SITEURL

TIMEZONE = "Europe/Paris"
DEFAULT_LANG = "en"
LOCALE = "en_US.utf-8"
DEFAULT_DATE_FORMAT = "%b %d, %Y"

# Feed generation is usually not desired when developing
FEED_RSS = "feeds/rss.xml"
FEED_ALL_ATOM = "feeds/all.atom.xml"
TRANSLATION_FEED_ATOM = None
RSS_FEED_SUMMARY_ONLY = False
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
DISPLAY_CATEGORIES = True

PATH = "content"
STATIC_PATHS = ["images"]
THEME = abspath(join(dirname(__file__), "themes", "pelican-hss"))

USER_LOGO_URL = "https://balthazar-rouberol.com/static/img/image-small.jpg"
TAGLINE = "I work with humans and computers."

# Blogroll
LINKS = ()

# Social widget
SOCIAL = [
    ("twitter", "https://twitter.com/brouberol"),
    ("github", "https://github.com/brouberol"),
    ("linkedin", "https://www.linkedin.com/in/balthazar-rouberol/"),
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["render_math"]

MARKDOWN = {
    "extensions": [
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.meta",
    ],
    "extension_configs": {"markdown.extensions.codehilite": {"css_class": "highlight"}},
}
