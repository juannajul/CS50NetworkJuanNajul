import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile


def index(request):

    if request.method == "POST":
        if request.user.is_anonymous:
           return HttpResponseRedirect(reverse('index')) 

        post_content = request.POST['content']
        new_post = Post(content=post_content, user=request.user)
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        posts= Post.objects.all().order_by("-id")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)  
        if request.user.is_authenticated:
            user_current = request.user
            current_user = get_object_or_404(User, username=user_current.username)
        else:
            current_user = None

        return render(request, "network/index.html", {
            "posts": page_obj,
            "current_user":current_user
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def profile_page(request, username):
    
    if request.user.is_anonymous:
        redirect('login')

    profile_user = get_object_or_404(User, username=username)
    current_user = request.user
    user_is_following_profileuser = False
    
    if request.user.is_authenticated:
        user_is_following_profileuser = current_user.following.filter(followed_id=profile_user.id).exists()

    profile_posts = Post.objects.filter(user=profile_user).order_by("id")
    paginator = Paginator(profile_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    num_posts = len(profile_posts)

    if request.user.is_authenticated:
        if request.method == "POST":
            if "follow_btn" in request.POST:
                Profile.objects.create(follower=current_user, followed=profile_user)
                user_is_following_profileuser = current_user.following.filter(followed_id=profile_user.id).exists()
            elif "unfollow_btn" in request.POST:
                Profile.objects.get(follower=current_user, followed=profile_user).delete()
                user_is_following_profileuser = current_user.following.filter(followed_id=profile_user.id).exists()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "current_user":current_user,
        "profile_posts": page_obj,
        "num_posts": num_posts,
        "user_is_following_profileuser":user_is_following_profileuser
    })


@login_required(login_url='login')
def following_page(request):
    user = request.user
    current_user = get_object_or_404(User, username=user.username)
    follower_user = Profile.objects.filter(follower=current_user)
    all_posts = Post.objects.all().order_by("-id")
    posts = []
    users_following = []
    for i in all_posts:
        for follower in follower_user:
            if follower.followed == i.user:
                posts.append(i)
                if i.user not in users_following:
                    users_following.append(i.user)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 

    return render(request, "network/following.html", {
        "posts" : page_obj,
        "current_user": current_user,
        "users_following": users_following
    })

@csrf_exempt
def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id, user=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # return posts:
    if request.user.is_anonymous:
        return HttpResponseRedirect('login')
    
    # Edit post content
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT":
        data_post = json.loads(request.body)
        if data_post.get("content") is not None:
            post.content = data_post["content"]
        post.save()
        return HttpResponse(status=204)
    
    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required(login_url='login')
@csrf_exempt
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post onr found."}, status=404)
    
    if request.user.is_anonymous:
        return HttpResponse('login')

    # Like post
    
    if request.method == "PUT":
        data_post = json.loads(request.body)
        if data_post.get("likes") is not None:
            if data_post.get("likes"):
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
        post.save()
        return HttpResponse(status=204)   
    elif request.method == "GET":
        return JsonResponse(post.serialize())
    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required"
        }, status=404)

def load_likes(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(pk=post_id)
        return JsonResponse(post.serialize())
    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required"
        }, status=404)