from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='/media/profile_img', blank=True)
    
    def _unicode__(self):
        return self.user.username
    
class BlogPost(models.Model):
    author = models.CharField(max_length = 30)
    title = models.CharField(max_length = 100)
    bodytext = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title
    
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=60)
    body = models.TextField()
    post = models.ForeignKey(BlogPost)

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))