from django.conf.urls.defaults import *
from django.views.generic import TemplateView
 

urlpatterns = patterns('main_site.views',
    (r'^$', 'main_page'),
    (r'^blog/$', 'displayBlog'),
    (r'^about/$', TemplateView.as_view(template_name="main_site/about.html")),
    (r'^add/$', 'add_post'),
    (r"^(\d+)/$", "blogComments"),
    (r"^add_comment/(\d+)/$", "add_comment"),
    (r'^profile/(?P<username>[a-zA-Z0-9_.-]+)/$', 'profile_disp'), 
)