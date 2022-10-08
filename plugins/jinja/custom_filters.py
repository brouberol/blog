from pelican.contents import Category, Tag


def single_word_capitalize(s):
    if len(str(s).split()) == 1:
        if isinstance(s, (Category, Tag)):
            s.name = s.name.capitalize()
    return s
