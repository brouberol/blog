#!/usr/bin/env python

from __future__ import unicode_literals

import os
from os.path import abspath, dirname, join

AUTHOR = "Balthazar Rouberol"
AUTHOR_TWITTER = "@brouberol"
AUTHOR_URL = "https://balthazar-rouberol.com"
SITENAME_FOR_META = "Balthazar - Blog"
SITENAME_FOR_READERS = "Balthazar"
SITENAME = SITENAME_FOR_READERS
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
CATEGORY_FEED_ATOM = "feeds/categories/{slug}.atom.xml"
TAG_FEED_ATOM = "feeds/tags/{slug}.rss.xml"
DISPLAY_CATEGORIES = True
ARTICLE_URL = "{slug}"

PATH = "content"
STATIC_PATHS = ["extra"]

extra_files = os.listdir(abspath(join(dirname(__file__), "content", "extra")))
EXTRA_PATH_METADATA = {
    "extra/%s" % (filename): {"path": "%s" % (filename)} for filename in extra_files
}

THEME = abspath(join(dirname(__file__), "themes", "pelican-hss"))

USER_LOGO_URL = "https://gravatar.com/avatar/6832e99e94636c4872030004c6f8fd70?s=180"
TAGLINE = "I work with humans and computers."

# Blogroll
LINKS = ()

# Social widget
SOCIAL = [
    ("github", "https://github.com/brouberol"),
    ("linkedin", "https://www.linkedin.com/in/balthazar-rouberol/"),
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

JINJA2CONTENT_TEMPLATES = ["../macros/jinja"]  # relative to the `content` directory
_JINJA2CONTENT_IGNORE = [
    "advent-of-code-day-3",
    "essential-tools-p4-customizing-shell",
    "rust-coverage-reports",
]
JINJA2CONTENT_IGNORE = [
    abspath(join(dirname(__file__), "content", path + ".md"))
    for path in _JINJA2CONTENT_IGNORE
]

PLUGIN_PATHS = ["plugins/pelican", "plugins"]
PLUGINS = ["render_math", "jinja"]

MARKDOWN = {
    "extensions": [
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.meta",
        "plugins.markdown.async_img:AsyncDecodedImgExtension",
        "markdown.extensions.toc",
    ],
    "output_format": "html5",
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.toc": {
            "title": "Table of Contents",
        },
    },
}
