# Create your views here.
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.db.models import Q
from django.template.context import RequestContext

from sphene.sphboard.models import Category, Post, POST_STATUSES

class SpheneModelInitializer:
    def __init__(self, request):
        self.request = request

    def init_model(self, model):
        model.do_init( self, self.request.session, self.request.user )
        

def showCategory(request, group = None, category_id = None, showType = None):
    args = {
        'group__isnull': True,
        'parent__isnull': True,
        }
    categoryObject = None
    if category_id != None and category_id != '0':
        args['parent__isnull'] = False
        args['parent'] = category_id
        categoryObject = Category.objects.get( pk = category_id )
    if group != None:
        args['group__isnull'] = False
        args['group'] = group

    if showType == 'threads':
        categories = []
    else:
        categories = Category.objects.filter( **args ).add_initializer( SpheneModelInitializer(request) )
    
    context = { 'rootCategories': categories,
                'category': categoryObject,
                'allowPostThread': categoryObject and categoryObject.allowPostThread( request.user ),
                'category_id': category_id, }
    templateName = 'sphene/sphboard/listCategories.html'
    if categoryObject == None:
        if showType != 'threads':
            return render_to_response( templateName, context,
                                       context_instance = RequestContext(request) )
        if group != None: thread_args = { 'category__group': group }
        else: thread_args = { 'category__group__isnull': True }
        thread_args[ 'thread__isnull'] = True
        context['isShowLatest'] = True
        thread_list = Post.objects.filter( **thread_args )
    else:
        thread_list = categoryObject.thread_list()

    thread_list = thread_list.extra( select = { 'latest_postdate': 'SELECT MAX(postdate) FROM sphboard_post AS postinthread WHERE postinthread.thread_id = sphboard_post.id OR postinthread.id = sphboard_post.id', 'is_sticky': 'status & %d' % POST_STATUSES['sticky'] } ).add_initializer( SpheneModelInitializer(request) )
    if showType != 'threads':
        thread_list = thread_list.order_by( '-is_sticky', '-latest_postdate' )
    else:
        thread_list = thread_list.order_by( '-latest_postdate' )

    return object_list( request = request,
                        queryset = thread_list,
                        template_name = templateName,
                        extra_context = context,
                        template_object_name = 'thread',
                        allow_empty = True,
                        paginate_by = 10,
                        )

def showThread(request, thread_id, group = None):
    thread = Post.objects.get( pk = thread_id )
    thread.touch( request.session, request.user )
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

def options(request, thread_id, group = None):
    thread = Post.objects.get( pk = thread_id )

    if request['cmd'] == 'makeSticky':
        thread.set_sticky(True)
    elif request['cmd'] == 'removeSticky':
        thread.set_sticky(False)

    thread.save()
    
    return HttpResponseRedirect( '../../thread/%s/' % thread.id )

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
    return HttpResponseRedirect( '../thread/%s/' % thread.id )
