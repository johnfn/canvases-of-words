from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'canvases.views.home', name='home'),
    # url(r'^canvases/', include('canvases.foo.urls')),

    #home
    url(r'^$', 'canvases.posts.views.home'),

    # === USERS ===


    # AUTHENTICATION

    #login page
    url(r'^login/$', 'canvases.users.views.login_user'),

    #logout
    url(r'^logout/$', 'canvases.users.views.logout_user'),

    #login post
    url(r'^postlogin/$', 'canvases.users.views.authenticate_user'),

    #register new user
    url(r'^register/$', 'canvases.users.views.register'),

    #submit registration
    url(r'^postregister/$', 'canvases.users.views.create_user'),

    #generic login required page
    url(r'^login_required/$', 'canvases.users.views.login_required'),

    # INFO

    #user page (generic)
    #TODO this should redirect to the page below...)
    url(r'^users/([a-zA-Z0-9]+)/$', 'canvases.users.views.user_detail'),

    url(r'me/', 'canvases.users.views.current_user_detail'),


    # === POSTS ===

    #write new post
    url(r'^writepost/$', 'canvases.posts.views.writepost'),

    #submit it
    url(r'^postsubmit/$', 'canvases.posts.views.newpost'),

    #post detail
    url(r'^([0-9]+)/$', 'canvases.posts.views.detail'),

    #edit post
    url(r'^([0-9]+)/edit/$', 'canvases.posts.views.edit_post'),

    #edit post, POST
    url(r'^postedit/$', 'canvases.posts.views.edit_post_post'),

    #view all posts

    #most recent
    url(r'^posts/$', 'canvases.posts.views.posts'),

    #specific page
    url(r'^posts/([0-9]+)/$', 'canvases.posts.views.posts_page'),

    # === GROUPS ===

    #view all groups
    url(r'^allgroups/$', 'canvases.groups.views.group_view_all'),

    #new group
    url(r'^newgroup/$', 'canvases.groups.views.group_new'),

    #new group POST
    url(r'^postnewgroup/$', 'canvases.groups.views.group_new_post'),

    #maintain group
    url(r'^group/([0-9]+)/$', 'canvases.groups.views.group_change'),

    #add member POST
    url(r'^group/([0-9]+)/addmember/$', 'canvases.groups.views.group_add_member_post'),

    #add post to group
    url(r'^group/([0-9]+)/newpost/$', 'canvases.posts.views.new_post_group'),

    #add post to group POST
    url(r'^group/([0-9]+)/newpostpost/$', 'canvases.posts.views.new_post_group_post'),


    # === COMMENTS ===

    #leave new comment
    url(r'^leavecomment/$', 'canvases.posts.views.leave_comment'),
    


    # Admin stuff
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
