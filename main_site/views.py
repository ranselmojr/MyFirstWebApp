from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from models import BlogPost, Comment
from forms import BlogPostForm, CommentForm, UserProfileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test, login_required


DEBUG = 10
INFO = 20
SUCCESS = 25
WARNING = 30
ERROR = 40

def main_page(request):
    return direct_to_template(request, 'main_site/index.html')


def my_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/main/')

        else:
            messages.add_message(request, WARNING , 'Username/Password Error')
            return HttpResponseRedirect('/main/')

    else:
        messages.add_message(request, WARNING , 'Username/Password Error')
        return HttpResponseRedirect('/main/')

def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/main/')
    


def create_new_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    
    try:
        user_exist = User.objects.get(username=request.POST['username'])
        if user_exist:     
            messages.add_message(request, WARNING , 'User Already exist')
            return HttpResponseRedirect('/main/')
    except ObjectDoesNotExist:
        user = User.objects.create_user(username, email, password)
        user.is_active = True
        user.save()
        messages.add_message(request, SUCCESS, 'Account Created')
        return HttpResponseRedirect('/main/')

def displayBlog(request):
    posts = BlogPost.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 2)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    
    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    
    #messages.add_message(request, SUCCESS, ' %s %s' %(posts, all_entrier.))
    context = RequestContext(request)
    return render_to_response('blog/blog.html', dict(posts=posts, user=request.user))

@login_required(login_url='/main/blog/')
@user_passes_test(lambda u: u.is_staff == True, login_url = '/main/blog/')
def add_post(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = BlogPostForm(request.POST) 
        if form.is_valid():
            blog = BlogPost()
            blog.author = request.user
            blog.title = request.POST['title']
            blog.bodytext = request.POST['bodytext']
            blog.save()
            messages.add_message(request, SUCCESS, 'Post Added')
            
            return HttpResponseRedirect('/main/blog/')
        else:
            messages.add_message(request, SUCCESS, 'Enter a valid Post')
            return HttpResponseRedirect('/main/add/')
    else:
        form = BlogPostForm() 
    return render_to_response('blog/add.html', {'form': form}, context)

def blogComments(request, pk):
    """Single post with comments and a comment form."""
    post = BlogPost.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post).order_by('-created')
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response("blog/comments.html", d)

def add_comment(request, pk):
    """Add a new comment."""
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]

        comment = Comment(post=BlogPost.objects.get(pk=pk))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()
    return HttpResponseRedirect(reverse("main_site.views.blogComments", args=[pk]))

def profile_disp(request, username):
    context = RequestContext(request)
    current_user = User.objects.get(username = username)
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = current_user
            profile.save()
                   
    else:
        profile_form = UserProfileForm()

    
        
    return render_to_response("main_site/profile.html", {'profile_form': profile_form}, context)
    

        


