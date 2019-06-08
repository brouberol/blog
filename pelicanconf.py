#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import platform
from os.path import abspath, join, dirname
AUTHOR = u'Balthazar Rouberol'
SITENAME = u'Balthazar'
if platform.node() in ['morenika', 'Balthazars-MacBook-Pro.local']:
    SITEURL = 'http://localhost:8000'
else:
    SITEURL = 'https://blog.balthazar-rouberol.com'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u"en"
LOCALE = 'en_US.utf-8'

# Feed generation is usually not desired when developing
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
TRANSLATION_FEED_ATOM = None
RSS_FEED_SUMMARY_ONLY = False
STATIC_PATHS = ['images', ]
THEME = abspath(join(dirname(__file__), 'themes', 'pelican-hyde'))
PROFILE_IMAGE = 'https://balthazar-rouberol.com/static/img/image-small.jpg'
BIO = 'I work with humans and computers.'

# Blogroll
LINKS = ()

# Social widget
SOCIAL = [
    ('home', 'https://balthazar-rouberol.com'),
    ('twitter', 'https://twitter.com/brouberol'),
    ('github', 'https://github.com/brouberol'),
    ('linkedin', 'https://www.linkedin.com/in/balthazar-rouberol/'),
]


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

DISQUS_SITENAME = 'balthazar-blog'
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ['render_math']
