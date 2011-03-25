from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from canvases.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import datetime

def home(request):
  return render_to_response('index.html',
    { 'posts' : Post.objects.all()
    , 'user' : request.user
    }
  )

def detail(request, id):
  return render_to_response('detail.html', {'post' : Post.objects.get(id=id)})

@login_required
def writepost(request):
  return render_to_response('writepost.html', {'user' : request.user}, context_instance=RequestContext(request))

#put a new post into the database
@login_required
def newpost(request):

  response = ""
  if "content" in request.POST:
    content = request.POST.get("content")

    post = Post(content=content, date=datetime.datetime.now(), creator=request.user)
    post.save()

    response = "Post successful."
  else:
    response = "I didn't get a post!"
  
  return HttpResponse(response)

def posts(request):
  return posts_page(request, -1)

class Link:
  pass

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

  return render_to_response('allposts.html', 
         { 'posts' : pages.page(which).object_list
         , 'pages' : pagelinks})

@login_required
def leave_comment(request):
  print request
  return HttpResponse("Lol")