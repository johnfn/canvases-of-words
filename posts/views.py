from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from canvases.posts.models import Post, Response
from canvases.groups.models import Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import datetime

def home(request):
  #TODO: Logout somewhere.
  if request.user.is_authenticated():
    return HttpResponseRedirect('/me/')
  
  return render_to_response('index.html',
    { 'posts' : Post.objects.all()
    , 'user' : request.user
    },
    context_instance=RequestContext(request))

def detail(request, id):
  #TODO: What happens when you aren't logged in?
  parent = Post.objects.filter(id=id)
  return render_to_response('detail.html', 
       { 'post'     : Post.objects.get(id=id)
       , 'user'     : request.user
       , 'comments' : Response.objects.filter(parent=parent) 
       }, 
       context_instance=RequestContext(request))

@login_required
def writepost(request):
  return render_to_response('writepost.html', 
        { 'user' : request.user
        , 'posturl' : "/postsubmit/" % (id)
        }, 
        context_instance=RequestContext(request))

#put a new post into the database
@login_required
def newpost(request):
  response = ""
  if "content" in request.POST:
    content = request.POST.get("content")
    title = request.POST.get("title")

    post = Post( content = content
               , title   = title
               , date    = datetime.datetime.now()
               , creator = request.user
               )
    post.save()

    response = "Post successful."
  else:
    response = "I didn't get a post!"
  
  return HttpResponse(response)

@login_required
def new_post_group(request, id):
  return render_to_response('writepost.html', 
        { 'user'    : request.user
        , 'posturl' : "/group/%s/newpostpost/" % (id)
        },
        context_instance=RequestContext(request))


@login_required
def new_post_group_post(request, id):
  content = request.POST.get("content")
  title = request.POST.get("title")

  post = Post( content = content
             , title   = title
             , date    = datetime.datetime.now()
             , creator = request.user
             , group   = Group.objects.get(id=int(id))
             )
  post.save()

  return HttpResponseRedirect("/group/%s/" % (id))


def posts(request):
  return posts_page(request, -1)

class Link:
  pass

@login_required
def edit_post(request, which):
  #TODO: Verify correct user
  post = Post.objects.get(id=which)

  if post.creator != request.user:
    return HttpResponse("That post isn't yours to edit! :)")

  return render_to_response('edit.html', 
         { 'post' : post
         , }, 
         context_instance=RequestContext(request))

#POST request
@login_required
def edit_post_post(request):
  newcontent = request.POST.get('content')
  id = request.POST.get('postid')

  post = Post.objects.get(id=id)

  post.content = newcontent
  post.save()
  return HttpResponseRedirect("/%s" % id)


def posts_page(request, which):
  pages = Paginator(Post.objects.all()[::-1], 5)
  num_pages = pages.num_pages

  if which == -1:
    which = num_pages
  else:
    which = str(int(which) + 1)

  pagelinks = []
  for x in range(num_pages):
    l = Link()
    l.link = '/posts/' + str(x)
    l.number = str(x)
    pagelinks.append(l)

  posts = pages.page(which).object_list

  #Append the number of comments to each post
  for x in range(len(posts)):
    posts[x].num_comments = Response.objects.filter(parent=posts[x]).count()


  return render_to_response('allposts.html', 
         { 'posts' : posts
         , 'pages' : pagelinks})

@login_required
def leave_comment(request):
  post    = Post.objects.get(id=request.POST["postid"])
  content = request.POST["content"]
  comment = Response(content=content, parent=post, creator=request.user)

  comment.save()

  return HttpResponseRedirect("/%s" % request.POST["postid"])