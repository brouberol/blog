from jinja2 import pass_context
from markupsafe import Markup
from pelican.contents import Category, Tag


def single_word_capitalize(s):
    if len(str(s).split()) == 1:
        if isinstance(s, (Category, Tag)):
            if not s.name.isupper():
                s.name = s.name.capitalize()
    return s


@pass_context
def subrender(context, value):
    _template = context.eval_ctx.environment.from_string(value)
    result = _template.render(**context)
    if context.eval_ctx.autoescape:
        result = Markup(result)
    return result
