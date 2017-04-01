from django import template
from django.utils.html import mark_safe
import re

register = template.Library()

'''
Takes in a block of text to be highlighted and a space-seperated ngram to highlight
'''
#@register.filter
# def highlight(text, ngram):
#     def findall(string, sub, listindex=[], offset=0):
#         i = string.find(sub, offset)
#         while i >= 0:
#             listindex.append(i)
#             i = string.find(sub, i + 1)
#         return listindex
# 
#     formated_text = text
#     for word in ngram.split():
#         starts = findall(formated_text.lower(), word)
#         ends = [i+ len(word) for i in starts]
#         
#         for i, j  in enumerate(starts):
#             start = int(starts[i])
#             end = int(ends[i])
#             formated_text = formated_text[:start] + "<span class='highlight'>" + formated_text[start:end] + "</span>" + formated_text[end:]
#     return mark_safe(formated_text)

@register.filter(name='highlight')
def highlight_filter(value, arg):
    return highlight(value, arg)['highlighted']

def highlight(text, ngram, ignore_case=None, word_boundary=None, class_name=None):
    phrases = ngram.split()
    if isinstance(phrases, str):
        phrases = [phrases]
    if ignore_case is None:
        ignore_case = True
    if word_boundary is None:
        word_boundary = True 
    if class_name is None:
        class_name = 'highlight'
        
    phrases = map(re.escape, phrases)
    flags = ignore_case and re.I or 0
    re_template = word_boundary and r"\b(%s)\b" or r"(%s)"
    expr = re.compile(re_template % "|".join(phrases), flags)
    template = '<span class="%s">%%s</span>' % class_name
    matches = []
    
    def replace(match):
        matches.append(match)
        return template % match.group(0)
    
    highlighted = mark_safe(expr.sub(replace, text))
    count = len(matches)
    return dict(original=text, highlighted=highlighted, hits=count)
