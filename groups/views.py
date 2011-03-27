from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from canvases.groups.models import Group
from canvases.posts.models import Post
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
import datetime


@login_required
def group_new(request):
  return render_to_response('newgroup.html'
                           , {}
                           , context_instance=RequestContext(request)
                           )

def group_view_all(request):
  return render_to_response('allgroups.html'
                           , { 'groups' : Group.objects.filter(visible=True)
                             }
                           , context_instance=RequestContext(request)
                           )

@login_required
def group_new_post(request):
  name = request.POST['name']
  description = request.POST['description']
  visible = ('visible' in request.POST)

  new_group = Group( name        = name
                   , description = description
                   , visible     = visible
                   )
 
  new_group.save() #have to get ID
  new_group.users.add(request.user)
  new_group.save()

  return HttpResponseRedirect("/group/%d" % (new_group.id))


#Get a list of all users. Convenient for autocomplete.
#Once we get a significant amount of users, we might have to change
#this up a little :P 
def get_all_users_array():
  user_list = User.objects.all()
  user_list = map(lambda user: '"%s"' % user.username, user_list)
  user_list = ", ".join(user_list)
  return "[ %s ]" % user_list

#The main group page.
@login_required
def group_change(request, id):
  #TODO: Check to see if you are a member.
  group = Group.objects.get(id=int(id))

  if group.users.filter(id=request.user.id).count() == 0:
    return HttpResponse("You don't belong to that group.")

  #Get all posts by all members of the group.
  posts = Post.objects.filter(group=group).order_by('-date')
  all_users = get_all_users_array()

  return render_to_response('group_detail.html'
                           , { 'group'     : group
                             , 'posts'     : posts
                             , 'all_users' : all_users
                             }
                           , context_instance=RequestContext(request)
                           )

@login_required
def group_add_member_post(request, id):
  print request.POST
  new_member = request.POST['name']

  try:
    user = User.objects.get(username=new_member)
  except:
    return HttpResponse("That user doesn't exist!")
  
  group = Group.objects.get(id=id)

  group.users.add(user)
  group.save()
  return HttpResponse(request.POST['name'])
  #return HttpResponseRedirect("/group/%s" % (id))


def ajax_test(request):
  print "ajax got %s" % request.POST
  return HttpResponse("HEYO")

