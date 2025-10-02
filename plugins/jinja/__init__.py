from pelican import signals

from .custom_filters import single_word_capitalize, subrender, s3_img_abspath
from .custom_globals import responsive_image
from .jinja2content_custom import JinjaMarkdownReader


def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({"single_word_capitalize": single_word_capitalize,  "s3_img_abspath": s3_img_abspath})


def add_all_globals(readers):
    readers.settings["JINJA_GLOBALS"].update({"responsive_image": responsive_image})
    readers.settings["JINJA_FILTERS"].update({"subrender": subrender})


def add_reader(readers):
    for ext in JinjaMarkdownReader.file_extensions:
        readers.reader_classes[ext] = JinjaMarkdownReader


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_all_filters)
    signals.readers_init.connect(add_reader)
    signals.readers_init.connect(add_all_globals)
