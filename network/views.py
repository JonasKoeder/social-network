from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Follow


def index(request):
    posts = Post.objects.all()
    
    # Pagination: 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content
            )
            return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseRedirect(reverse("index"))


def profile(request, username):
    # Get the user
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/error.html", {
            "message": "User not found."
        })
    
    # Get all posts of this user
    posts = Post.objects.filter(author=profile_user)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Check if current user follows this user
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=profile_user
        ).exists()
    
    # Count followers and following
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count
    })


@login_required
def follow(request, username):
    if request.method == "POST":
        try:
            user_to_follow = User.objects.get(username=username)
            
            # You cannot follow yourself
            if user_to_follow != request.user:
                # Toggle follow/unfollow
                follow_instance = Follow.objects.filter(
                    follower=request.user,
                    following=user_to_follow
                )
                
                if follow_instance.exists():
                    # Unfollow
                    follow_instance.delete()
                else:
                    # Follow
                    Follow.objects.create(
                        follower=request.user,
                        following=user_to_follow
                    )
        except User.DoesNotExist:
            pass
        
        return HttpResponseRedirect(reverse("profile", args=[username]))
    
    return HttpResponseRedirect(reverse("index"))

    
@login_required
def following(request):
    # Get all users that the current user follows
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    
    # Get all posts of the following users
    posts = Post.objects.filter(author__in=following_users)
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
            
            # Security check: Only the author can edit their post
            if post.author != request.user:
                return JsonResponse({"error": "Not authorized"}, status=403)
            
            # Load new data
            data = json.loads(request.body)
            new_content = data.get("content", "")
            
            if new_content:
                post.content = new_content
                post.save()
                return JsonResponse({"message": "Post updated", "content": post.content}, status=200)
            else:
                return JsonResponse({"error": "Content cannot be empty"}, status=400)
                
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
    
    return JsonResponse({"error": "PUT request required"}, status=400)


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

@csrf_exempt
@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=post_id)
            
            # Toggle like/unlike
            if request.user in post.likes.all():
                # Unlike
                post.likes.remove(request.user)
                liked = False
            else:
                # Like
                post.likes.add(request.user)
                liked = True
            
            return JsonResponse({
                "liked": liked,
                "like_count": post.like_count()
            }, status=200)
            
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
    
    return JsonResponse({"error": "POST request required"}, status=400)