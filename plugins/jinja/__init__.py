from pelican import signals

from .custom_filters import single_word_capitalize
from .jinja2content_custom import JinjaMarkdownReader


def add_all_filters(pelican):
    """Add (register) all filters to Pelican."""
    pelican.env.filters.update({"single_word_capitalize": single_word_capitalize})


def add_reader(readers):
    for ext in JinjaMarkdownReader.file_extensions:
        readers.reader_classes[ext] = JinjaMarkdownReader


def register():
    """Plugin registration."""
    signals.generator_init.connect(add_all_filters)
    signals.readers_init.connect(add_reader)
