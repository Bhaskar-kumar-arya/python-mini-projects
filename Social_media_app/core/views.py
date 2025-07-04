from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following = FollowersCount.objects.filter(follower = request.user)
    posts = []
    for follow in user_following:
        user_posts = Post.objects.filter(user=follow.user).order_by('-created_at')
        for post in user_posts:
            posts.append(post)
    return render(request, 'index.html',{'user_profile' : user_profile,'posts' : posts})

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST' :
        follower = request.POST.get('follower') 
        username = request.POST.get('user')
        user_obj = User.objects.get(username=username)
        follower_obj = User.objects.get(username=follower)
        if followercount := FollowersCount.objects.filter(follower=follower_obj,user=user_obj).first():
            followercount.delete()
            return redirect('/profile/' + username)
        else :
            new_follower = FollowersCount.objects.create(follower=follower_obj,user=user_obj)   
            new_follower.save()
            return redirect('/profile/' + username)
    else :
        return redirect('/')

@login_required(login_url='signin')    
def settings (request) :
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profileImage = request.FILES.get('profileImage')
        user_bio = request.POST.get('bio')
        user_location = request.POST.get('location')
        if user_profileImage:
            user_profile.profileimg = user_profileImage
        user_profile.bio = user_bio
        user_profile.location = user_location
        user_profile.save()       
        return redirect('settings') 
    return render(request,'settings.html',{'user_profile' : user_profile})

@login_required(login_url='signin')
def upload(request): 
    if request.method == "POST" : 
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        if not image or not caption:
            messages.error(request, "Please provide both an image and a caption.")
            return 
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        password2 = request.POST.get('password2') 
        email = request.POST.get('email')
        print(username, password, email)

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        user = User.objects.create_user(username=username,password=password,email=email)
        user.save()
        user_login = auth.authenticate(username = username,password=password)
        auth.login(request,user_login)
        # create a profile for the user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user = user_model)
        new_profile.save()
        return redirect('settings')
    else :
        return render(request, 'signup.html')

def signin (request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password = password)
        if user :
            auth.login(request,user)
            return redirect('/')
        else :
            messages.error(request,'invalid credentials')
            return redirect('signin')
    else :
        return render(request,'signin.html')    

@login_required(login_url='signin')
def like_post(request):
    user = request.user
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(user=user).first()
    if not like_filter:
        new_like = LikePost.objects.create(user=user, post=post)
        post.no_of_likes += 1
        post.save()
        new_like.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request,pk) :
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user = user_object)
    user_no_of_posts = len(user_posts)
    is_following = False
    if FollowersCount.objects.filter(follower=request.user, user=user_object).first():
        is_following = True
    user_followersCount = len(FollowersCount.objects.filter(user=user_object))   
    user_followingCount = len(FollowersCount.objects.filter(follower=user_object))    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_no_of_posts' : user_no_of_posts,
        'is_following' : is_following,
        'user_followersCount' : user_followersCount,
        'user_followingCount' : user_followingCount,
    }
    return render(request,'profile.html',context)    

@login_required(login_url='signin')    
def logout (request) :
    auth.logout(request)
    return redirect('signin')    
