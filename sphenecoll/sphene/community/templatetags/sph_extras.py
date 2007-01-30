from django import template

register = template.Library()

@register.filter
def sph_markdown(value, arg=''):
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError, "Error in {% markdown %} filter: The Python markdown library isn't installed."
        return value
    else:
        save_mode = arg == 'safe'
        md = markdown.Markdown(value,
                                 extensions = [ 'footnotes', 'wikilink' ],
                                 extension_configs = { 'wikilink': [ ( 'base_url', '' ),
                                                                    ]},
                                 )
        return md.toString()

