from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from canvases.groups.models import Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, models, login, logout
import datetime


@login_required
def group_new(request):
  return render_to_response('newgroup.html', {}, context_instance=RequestContext(request))

@login_required
def group_new_post(request):
  name = request.POST['name']
  description = request.POST['description']

  new_group = Group( name        = name
                   , description = description
                   )
 
  new_group.save()
  return HttpResponseRedirect("/group/%d" % (new_group.id))

@login_required
def group_change(request, id):
  group = Group.objects.filter(id=int(id))

  return render_to_response('changegroup.html', 
                           { 'group' : group 
                           ,
                           },
                           context_instance=RequestContext(request))