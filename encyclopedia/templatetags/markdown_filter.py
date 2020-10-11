from django import template 
from markdownx.utils import markdownify

import markdown

register = template.Library()


@register.filter
def markdownify(text):
    return markdown.markdown(text, safe_mode='escape')