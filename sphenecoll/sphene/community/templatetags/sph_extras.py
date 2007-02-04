from django import template
from time import strftime

from sphene.sphwiki.models import WikiAttachment

register = template.Library()

class SimpleHelloWorldMacro (object):
    def handleMacroCall(self, doc, params):
        return doc.createTextNode("Hello World!")

class ImageMacro (object):
    def handleMacroCall(self, doc, params):
        if params.has_key( 'id' ):
            attachment = WikiAttachment.objects.get( id = params['id'] )
            el = doc.createElement( 'img' )
            el.setAttribute( 'src', attachment.get_fileupload_url() )
            for paramName in [ 'width', 'height', 'alt', 'align' ]:
                if params.has_key( paramName ):
                    el.setAttribute( paramName, params[paramName] )
            return el
        return doc.createTextNode("<b>Error, no 'id' given for img macro.</b>")

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
                                 extensions = [ 'footnotes', 'wikilink', 'macros' ],
                                 extension_configs = { 'wikilink': [ ( 'base_url', '../' ),
                                                                    ],
                                                       'macros': [ ( 'macros',
                                                                     { 'helloWorld': SimpleHelloWorldMacro(),
                                                                       'img': ImageMacro(), } )]},
                                 )
        return md.toString()

@register.filter
def sph_date(value):
    return value.strftime( "%Y-%m-%d %H:%M:%S" )

