#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import platform
from os.path import abspath, join, dirname
AUTHOR = u'Balthazar Rouberol'
SITENAME = u'Balthazar'
if platform.node() == 'morenika':
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
STATIC_PATHS = ['images', ]
THEME = abspath(join(dirname(__file__), 'themes', 'aboutwilson'))

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

DISQUS_SITENAME = 'balthazar-blog'
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ['render_math']
