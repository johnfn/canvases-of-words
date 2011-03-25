from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from canvases.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, models, login, logout
import datetime

def register(request):
  return render_to_response('register.html', {}, context_instance=RequestContext(request))

def create_user(request):
  if User.objects.filter(username=request.POST.get('username')).count() > 0:
    return HttpResponse("That username is already taken!")

  newuser = User.objects.create_user(request.POST.get('username'), 
                                     request.POST.get('email')   , 
                                     request.POST.get('password'))
  newuser.save()

  #TODO: Redirect
  return HttpResponse('New user created.')

def user_detail(request, user_string):
  user_obj = User.objects.filter(username=user_string)
  posts = Post.objects.filter(creator=user_obj)[::-1]

  return render_to_response('user_detail.html', 
    { 'username' : user_string
    , 'posts'    : posts
    })

#TODO potential name conflict with @login_required decorator
def login_required(request):
  return HttpResponse("You have to log in to do that.")

def logout_user(request):
  logout(request)

  #TODO: Redirect
  return HttpResponse("Successfully logged out.")

def login_user(request):
  return render_to_response('login.html', {}, context_instance=RequestContext(request))

def authenticate_user(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      return HttpResponse("Successfully logged in. Go write something!")

      #TODO
      #return HttpResponseRedirect(main page)
    else:
      return HttpResponse("That's weird. Come ask me what happened.")
  else:
    return HttpResponse("Username or password incorrect.")