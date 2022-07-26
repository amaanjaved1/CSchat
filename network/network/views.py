from http.client import HTTPResponse
import json
from unittest import result
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm, TextInput, ValidationError
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from itertools import chain
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


class NewPostForm(ModelForm):
    class Meta: 
        model = Post
        fields = ["subject", "content"]

def index(request, page_id):
    posts = Post.objects.order_by("-post_date").all()
    pages = Paginator(posts, 10)
    current_page = pages.page(page_id)
    if current_page.has_next() == True:
        nextpage = True
        nextpagenum = page_id + 1
    elif current_page.has_next() == False: 
        nextpage = False
        nextpagenum = 1
    if current_page.has_previous() == True:
        previouspage = True
        previouspagenum = page_id - 1
    elif current_page.has_previous() == False:
        previouspage = False
        previouspagenum = 1
    return render(request, "network/index.html", {
        "posts": current_page, 
        "pagenum": page_id,
        "nextpage": nextpage,
        "previouspage": previouspage,
        "nextpagenum": nextpagenum, 
        "previouspagenum": previouspagenum,
        "display_type": "All Posts",
        "index": True,
        "user": request.user,
        "editing_post": False
    })

def home(request):
    page_id = 1
    posts = Post.objects.order_by("-post_date").all()
    pages = Paginator(posts, 10)
    current_page = pages.page(page_id)
    if current_page.has_next() == True:
        nextpage = True
        nextpagenum = page_id + 1
    elif current_page.has_next() == False: 
        nextpage = False
        nextpagenum = 1
    if current_page.has_previous() == True:
        previouspage = True
        previouspagenum = page_id - 1
    elif current_page.has_previous() == False:
        previouspage = False
        previouspagenum = 1
    return render(request, "network/index.html", {
        "posts": current_page, 
        "pagenum": page_id,
        "nextpage": nextpage,
        "previouspage": previouspage,
        "nextpagenum": nextpagenum, 
        "previouspagenum": previouspagenum,
        "display_type": "All Posts",
        "index": True,
        "editing_post": False
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
            return HttpResponseRedirect(reverse("index", args=(1,)))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", args=(1,)))


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
        return HttpResponseRedirect(reverse("index", args=(1,)))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def add(request):
    if request.method == "GET":
        return render(request, "network/add.html", {
            "form": NewPostForm
        }) 
    else: 
        form = NewPostForm(request.POST)
        user = request.user
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            Post(subject=subject, content=content, poster=user).save()
            return HttpResponseRedirect(reverse("index", args=(1,)))
        else: 
            return render(request, "network/add.html", {
                "form": form,
                "message": "Invalid Submission"
            })

@login_required(login_url='login')
def profile(request, user_id):
    try:
        profile = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User Not Found")
    else: 
        if request.method == "GET":
            user = request.user
            posts = profile.posted_posts.order_by("-post_date").all()
            if user_id == user.id:
                owner = True
                following_profile = None
            else:
                owner = False
                if user in profile.followers.all():
                    following_profile = True
                else: 
                    following_profile = False
            return render(request, "network/profile.html", {
                "profile": profile,
                "posts": posts,
                "owner": owner,
                "following": profile.following.all(),
                "followers": profile.followers.all(),
                "following_profile": following_profile
            }) 


@login_required(login_url='login')
def following(request, page_id):
    if request.method == "GET":
        all_query_sets = [] #create an empty list 
        for each in request.user.following.all(): #add a query set of each followed users posts
            if each != request.user:
                all_query_sets.append(each.posted_posts.all())
        result_list = list(chain(*all_query_sets)) #combine all objects into a list 
        result_list.sort(key=lambda x: x.post_date, reverse=True) #sort by date
        pages = Paginator(result_list, 10) 
        current_page = pages.page(page_id)
        if current_page.has_next() == True:
            nextpage = True
            nextpagenum = page_id + 1
        elif current_page.has_next() == False: 
            nextpage = False
            nextpagenum = 1
        if current_page.has_previous() == True:
            previouspage = True
            previouspagenum = page_id - 1
        elif current_page.has_previous() == False:
            previouspage = False
            previouspagenum = 1
        return render(request, "network/index.html", {
        "posts": result_list, 
        "pagenum": page_id,
        "nextpage": nextpage,
        "previouspage": previouspage,
        "nextpagenum": nextpagenum, 
        "previouspagenum": previouspagenum,
        "display_type": "Following",
        "index": False,
        "user": request.user,
        "follow_len": len(result_list),
        "editing_post": False
    })
    
@csrf_exempt
@login_required(login_url='login')
def likes(request, post_id):
    try: 
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist: 
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action", "")
        if action == "like":
            post.likes.add(request.user)
        else: 
            post.likes.remove(request.user)
        return JsonResponse(post.serialize())
    elif request.method == "GET":
        return JsonResponse(post.serialize())
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
@login_required(login_url='login')
def follow(request, profile_id):
    try: 
        profile = User.objects.get(id=profile_id)
    except User.DoesNotExist: 
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action", "")
        if action == "follow":
            profile.followers.add(request.user)
        else: 
            profile.followers.remove(request.user)
        return JsonResponse(profile.serialize())
    elif request.method == "GET":
        return JsonResponse(profile.serialize())
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
@login_required(login_url='login')
def edit(request, post_id):
    try: 
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist: 
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "POST":
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return JsonResponse(post.serialize())
    elif request.method == "GET":
        return JsonResponse(post.serialize())
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)