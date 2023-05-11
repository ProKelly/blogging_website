from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comments
from django.contrib.auth import login, authenticate, decorators
from .forms import RegistrationForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    posts = BlogPost.objects.all().order_by('-date_published')[:5]
    return render(request, 'home.html', {'posts':posts})

def post_detail(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    comments = post.comments.all().order_by('-date_posted')
    form = CommentForm()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.blogpost= post
            comments.author = request.user
            comments.save()
            return redirect('post_detail', pk=post.id)
    
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form':form})

@login_required
def profile(request):
    user = request.user
    posts = BlogPost.objects.filter(author=user).order_by('-date_published')
    comment = Comments.objects.filter(author=user).order_by('-date_posted')
    return render(request, 'profile.html', {'user':user, 'posts': posts, 'comment':comment})

@login_required 
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required
def delete_post(request, id):
    post = BlogPost.objects.get(pk=id)
    post.delete()
    return redirect('profile')
  
            
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form':form})