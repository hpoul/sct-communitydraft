# Create your views here.
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.db.models import Q
from django.template.context import RequestContext

from sphene.sphboard.models import Category, Post

def showCategory(request, group = None, category_id = None):
    args = {
        'group__isnull': True,
        'parent__isnull': True,
        }
    categoryObject = None
    if category_id != None and category_id != '0':
        args['parent__isnull'] = False
        args['parent'] = category_id
        categoryObject = Category.objects.get( pk = category_id )
    categories = Category.objects.filter( **args )
    """
    return render_to_response('sphene/sphboard/listCategories.html',
                              { 'rootCategories': categories,
                                'category': categoryObject,
                                'allowPostThread': categoryObject and categoryObject.allowPostThread( request.user ) })
                                """
    context = { 'rootCategories': categories,
                'category': categoryObject,
                'allowPostThread': categoryObject and categoryObject.allowPostThread( request.user ) }
    templateName = 'sphene/sphboard/listCategories.html'
    if categoryObject == None:
        return render_to_response( templateName, context,
                                   context_instance = RequestContext(request) )
    return object_list( request = request,
                        queryset = categoryObject.thread_list().order_by( '-postdate' ),
                        template_name = templateName,
                        extra_context = context,
                        template_object_name = 'thread',
                        allow_empty = True,
                        paginate_by = 3,
                        )

def showThread(request, thread_id, group = None):
    thread = Post.objects.get( pk = thread_id )
    #thread = get_object_or_404(Post, pk = thread_id )
    return object_list( request = request,
                        #queryset = Post.objects.filter( Q( pk = thread_id ) | Q( thread = thread ) ).order_by('postdate'),
                        queryset = thread.allPosts().order_by('postdate'),
                        allow_empty = True,
                        template_name = 'sphene/sphboard/showThread.html',
                        extra_context = { 'thread': thread,
                                          'allowPosting': thread.allowPosting( request.user ),
                                          'postSubject': 'Re: ' + thread.subject,
                                          },
                        template_object_name = 'post',
                        )


def post(request, group = None):
    thread = None
    category = None
    if 'thread' in request.POST:
        thread = get_object_or_404(Post, pk = request.POST['thread'])
        category = thread.category
    else:
        category = get_object_or_404(Category, pk = request.POST['category'])
    if not category.allowPostThread( request.user ): raise Http404;

    subject = request.POST['subject']
    body = request.POST['body']
    
    newpost = Post( category = category,
                    subject = subject,
                    body = body,
                    author = request.user,
                    thread = thread,
                    )
    newpost.save()
    request.user.message_set.create( message = "Post created successfully." )
    if thread == None: thread = newpost
    return HttpResponseRedirect( '../thread/%s' % thread.id )
