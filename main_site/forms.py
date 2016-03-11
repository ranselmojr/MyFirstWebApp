from django import forms
from main_site.models import BlogPost, Comment, UserProfile
from django.forms import ModelForm



class BlogPostForm(forms.Form):
   title = forms.CharField(max_length=100, help_text="Please Enter the Title ")
   bodytext = forms.CharField()
   
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
   
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #fields = ('website', 'picture')
        exclude = ["picture"]