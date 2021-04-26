import markdown2
from django.conf import settings

# markdownx.utils.markdownify

def markdownify2(content):
    print('ab')
    return markdown2.markdown(content, extras=[
        'markdown.extensions.tables',
        'pymdownx.magiclink',
        'pymdownx.betterem',
        'pymdownx.tilde',
        'pymdownx.emoji',
        'pymdownx.tasklist',
        'pymdownx.superfences',
        'pymdownx.saneheaders'
    ])


