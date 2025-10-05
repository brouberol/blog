"""
This is a copy of https://github.com/getpelican/pelican-plugins/blob/master/jinja2content/jinja2content.py
adding the ability of excluding some files from being processed, via the JINJA2CONTENT_IGNORE
global list.

"""

import os
import re
from tempfile import NamedTemporaryFile

from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from pelican.readers import MarkdownReader
from pelican.utils import pelican_open


class JinjaContentMixin(object):
    def __init__(self, *args, **kwargs):
        super(JinjaContentMixin, self).__init__(*args, **kwargs)

        # will look first in 'JINJA2CONTENT_TEMPLATES', by default the
        # content root path, then in the theme's templates
        local_dirs = self.settings.get("JINJA2CONTENT_TEMPLATES", ["."])
        local_dirs = [
            os.path.join(self.settings["PATH"], folder) for folder in local_dirs
        ]
        theme_dir = os.path.join(self.settings["THEME"], "templates")

        loaders = [FileSystemLoader(_dir) for _dir in local_dirs + [theme_dir]]
        if "JINJA_ENVIRONMENT" in self.settings:  # pelican 3.7
            jinja_environment = self.settings["JINJA_ENVIRONMENT"]
        else:
            jinja_environment = {
                "trim_blocks": True,
                "lstrip_blocks": True,
                "extensions": self.settings["JINJA_EXTENSIONS"],
            }
        self.env = Environment(loader=ChoiceLoader(loaders), **jinja_environment)
        if "JINJA_FILTERS" in self.settings:
            self.env.filters.update(self.settings["JINJA_FILTERS"])
        if "JINJA_GLOBALS" in self.settings:
            self.env.globals.update(self.settings["JINJA_GLOBALS"])
        if "JINJA_TEST" in self.settings:
            self.env.tests.update(self.settings["JINJA_TESTS"])

    def read(self, source_path):
        with pelican_open(source_path) as text:
            ## Here is the custom part: an escape hatch for some articles
            if source_path not in self.settings["JINJA2CONTENT_IGNORE"]:
                code_blocks = re.findall(r"```[\s\w]+\n[^`]+```\n", text)

                for i, code_block in enumerate(code_blocks):
                    text = text.replace(code_block, f"__CODEBLOCK__{i}__")

                text = self.env.from_string(text).render()

                for i, code_block in enumerate(code_blocks):
                    text = text.replace(f"__CODEBLOCK__{i}__", code_block)

        with NamedTemporaryFile(delete=False) as f:
            f.write(text.encode())
            f.close()
            content, metadata = super().read(f.name)
            os.unlink(f.name)
            return content, metadata


class JinjaMarkdownReader(JinjaContentMixin, MarkdownReader):
    pass
