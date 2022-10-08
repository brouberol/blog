from pelican.contents import Category


def single_word_capitalize(s):
    if len(str(s).split()) == 1:
        if isinstance(s, Category):
            s.name = s.name.capitalize()
    return s
