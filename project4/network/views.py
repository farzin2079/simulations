import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserForm
from .models import User, Post, Follow, Profile


def index(request):
    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(posts , 10)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)
    
    return render(request, "network/index.html", {
        'posts': page_objs,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match.",
                'forms': CustomUserForm
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken.",
                'forms': CustomUserForm
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html", {
            'forms': CustomUserForm
        })
    
@csrf_exempt
def follow(request, id):
    if (request.method == 'POST'):
        follower = request.user
        following = User.objects.get(pk=id)
        try:
            follow = Follow.objects.get(follower=request.user, following=id)
            follow.delete()
            return JsonResponse({"massage": "unfollow"})
        except:
            try:
                add = Follow(following=following, follower=follower)
                add.save()
                return JsonResponse({"massage": "followed"})
            
            except:
                return JsonResponse({"error": "serever error!"})
        
    else:
        try:
            follow = Follow.objects.get(follower=request.user, following=id)
            return JsonResponse({'followed':'true'})
        except:
            return JsonResponse({'followed':'false'})
        

def following(request):
    follower = request.user
    followings = Follow.objects.filter(follower=follower)
    posts = Post.objects.all()
    
    paginator = Paginator(posts , 10)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)
    
    return render(request, 'network/following.html',{
        'followings':followings,
        'posts':page_objs
        })
        
        
def profile(request, user_id):
    user = User.objects.get(pk=int(user_id))
    profile = Profile.objects.get( user = user)
    
    posts = Post.objects.filter(posted_by = user_id)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts , 10)
    page_num = request.GET.get('page')
    page_objs = paginator.get_page(page_num)
    
    
    return render(request, 'network/profile.html',{
        'profile':profile,
        'follower_count': follower_count(user_id),
        'following_count': following_count(user_id),
        'posts':page_objs,
    })
 
@csrf_exempt  
def like(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    exlikes = post.likes
    if (request.method == 'POST'):
        try:
            likes = Post.objects.get(like=user)
            likes.like.remove(user)
            post.likes = exlikes - 1
            post.save()
            return JsonResponse({'massage':'unlike'})
        except:
            post.like.add(user)
            post.likes = exlikes + 1
            post.save()
            return JsonResponse({'massage':'like'})
    else:
        try:
            Post.objects.get(liked=user)
            return JsonResponse({'liked':'true'})
        except:
            return JsonResponse({'liked':'false'})
    
def addpost(request):
    if (request.method == 'POST'):
        posted_by = request.user
        title = request.POST.get('title')
        body = request.POST.get('body')
        
        post = Post(posted_by=posted_by, title=title, body=body)
        post.save()
    return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
def edit(request, post_id):
    if (request.method == 'POST'):
        title = request.POST.get('title')
        body = request.POST.get('body')
        
        post = Post.objects.filter(pk = post_id, posted_by=request.user)
        post.update(title=title, body=body)
        
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def delete(request, post_id):
    if (request.method == 'POST'):
        try:
            Post.objects.get(pk = post_id).delete()
            return JsonResponse({'massage':'deleted'})
        except:
            return JsonResponse({'massage':'not deleted'})
    else:
        return HttpResponseRedirect(reverse("index"))
    
def follower_count(user_id):
    follower_count = Follow.objects.filter(following=int(user_id)).count
    return follower_count
     
def following_count(user_id):
    following_count = Follow.objects.filter(follower=int(user_id)).count        
    return following_count
        