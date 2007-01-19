from django import template

register = template.Library()

@register.filter
def sphrepeat(value, arg):
    ret = "";
    for x in range(arg):
        ret += value
    return ret

@register.filter
def sphminus(value, arg):
    return value-arg

@register.filter
def sphrange(value):
    return range( value )

@register.inclusion_tag('sphene/sphboard/_displayCategories.html')
def sphboard_displayCategories( categories, maxDepth = 5, level = -1 ):
    if maxDepth < level:
        return { }
    return {'categories': categories,
            'level'     : level + 1,
            'maxDepth'  : maxDepth}

@register.inclusion_tag('sphene/sphboard/_displayLatestPost.html')
def sphboard_latestPost( latestPost, showSubject = 1 ):
    return { 'latestPost' : latestPost, 'showSubject': showSubject }

def sphboard_displayBreadcrumbs( category = None, post = None ):
    if category == None:
        if post == None: return { }
        category = post.category
        current = post
    else:
        current = category
    breadcrumbs = []
    while category != None:
        breadcrumbs.insert(0, category)
        category = category.parent
    return { 'thread': post, 'categories': breadcrumbs, 'current': current }

@register.inclusion_tag('sphene/sphboard/_displayBreadcrumbs.html')
def sphboard_displayBreadcrumbsForThread( post ):
    return sphboard_displayBreadcrumbs( post = post )

@register.inclusion_tag('sphene/sphboard/_displayBreadcrumbs.html')
def sphboard_displayBreadcrumbsForCategory( category ):
    return sphboard_displayBreadcrumbs( category = category )

@register.inclusion_tag('sphene/sphboard/_displayUserName.html')
def sphboard_displayUserName( user ):
    return { 'user': user }

@register.inclusion_tag('sphene/sphboard/_pagination.html')
def sphboard_pagination( pages, page ):
    has_next = page < pages
    has_prev = page > 1
    return { 'page_range': range( 1, pages+1 ),
             'page': page,
             'pages': pages,
             'has_next': has_next,
             'has_prev': has_prev,
             'next': page + 1,
             'prev': page - 1,
             }
