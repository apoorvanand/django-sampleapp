from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import loader
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Post
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    template = loader.get_template('posts/index.html')
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return HttpResponse(template.render(context, request))

def detail(request, post_id):
    template = loader.get_template('posts/detail.html')
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
    }
    return HttpResponse(template.render(context, request))

def create(request):
    template = loader.get_template('posts/create.html')
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post(
                title=request.POST['title'],
                subtitle=request.POST['subtitle'],
                content=request.POST['content'],
                author=request.user,
            )
            post.save()
            return redirect('posts:detail', post_id=post.id)
        return HttpResponse(template.render({}, request))

def edit(request, post_id):
    template = loader.get_template('posts/edit.html')
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        context = {
            'post': post,
        }
        if post.author != request.user:
            return redirect('posts:detail', post_id=post.id)
        if request.method == 'POST':
            post.title = request.POST['title']
            post.subtitle = request.POST['subtitle']
            post.content = request.POST['content']
            post.save()
            return redirect('posts:detail', post_id=post.id)
        return HttpResponse(template.render(context, request))

def delete(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)
        if post.author == request.user:
            post.delete()
            return redirect('posts:index')
        else:
            return redirect('posts:detail', post_id=post.id)
        
    # else:
    #     return para a pagina de login
        

def signup(request):
    template = loader.get_template('posts/signup.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User()
        user.username = username
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('posts:index')
    else:
        return HttpResponse(template.render({}, request))

def signin(request):
    template = loader.get_template('posts/signin.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:index')
        else:
            return HttpResponse(template.render({}, request))
    return HttpResponse(template.render({}, request))

def signout(request):
    logout(request)
    return redirect('posts:index')

def post_list(request):
    posts_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) |Q(subtitle__icontains=query)
        ).distinct()
    paginator = Paginator(posts_list, 6) # 6 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }
    return render(request, "posts/post-list.html", context)