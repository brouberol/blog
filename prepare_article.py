#!/usr/bin/env python3

import sys
import re

filename = sys.argv[1]

LINK_PATTERN = r'!\[([^\]]+)\]\((.+)\)\n\n'
REPLACE_LINK_BY = '![\\1](\\2)\n<span class=imgcaption>\\1</span>\n\n'
SETEXT_H1_PATTERN = r'([\w\' ]+)\n(=){2,}'
ATX_H1_PATTERN = '# \\1'
SETEXT_H2_PATTERN = r'([^\n]+)\n(-){2,}'
ATX_H2_PATTERN = '## \\1'
TITLE_META_PATTERN = r"Title:\n"
LABEL_PATTERN = r'`\\label\{.+}`\{=tex\}'
SHELL_BLOCKQUOTE_PATTERN = r'``` *(console|shell|zsh|bash)'
SHELL_BLOCKQUOTE_REPLACE = '``` ext\\1'


with open(filename) as f:
    data = f.read()

    data = re.sub(r'’', "'", data)

    # Collapse multiline md image links
    for match in re.findall(LINK_PATTERN, data):
        data = data.replace(match[0], match[0].replace('\n', ' '))

    # Insert image captions
    data = re.sub(LINK_PATTERN, REPLACE_LINK_BY, data)

    m = re.search(SETEXT_H1_PATTERN, data)
    if m:
        title = m.group(1)
        data = re.sub(TITLE_META_PATTERN, "Title: " + title + '\n', data)

    # Replace h1 and h2 settext styles by ATX styles
    data = re.sub(SETEXT_H1_PATTERN, ATX_H1_PATTERN, data)
    data = re.sub(SETEXT_H2_PATTERN, ATX_H2_PATTERN, data)

    # Join the category
    data = data.replace("Aspiring Software\nDeveloper", "Aspiring Software Developer")

    # Remove latex labels
    data = re.sub(LABEL_PATTERN, '', data)

    data = re.sub(SHELL_BLOCKQUOTE_PATTERN, SHELL_BLOCKQUOTE_REPLACE, data)

    data = data.replace("## Exercices", "## Going further")

with open(filename, 'w') as out:
    out.write(data)
