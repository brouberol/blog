import sys
from os.path import join, abspath, dirname

sys.path.insert(0, abspath(join(dirname(__file__), "..", "pelican-plugins")))

from jinja2content import JinjaContentMixin


class ExtendedJinjaContentMixin(JinjaContentMixin):
    def read(self, source_path):
        if source_path not in self.settings["JINJA2CONTENT_EXCLUDE"]:
            return super().read(source_path)
