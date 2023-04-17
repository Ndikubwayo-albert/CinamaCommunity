from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Contactus,CreateUser,AddPost, Comment
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
import uuid
from .utils import send_verification_email 
import datetime 
import os



def HomePage(request):
    movies = AddPost.objects.all().order_by("-posted_time")[:3]
    context = {'movies': movies}
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_content = request.POST['message']
        
        new_contactus = Contactus(
            name=name, 
            email=email, 
            message=message_content
            )
        new_contactus.save()
        messages.info(request, 'message sent successfully')
        
    return render(request,'index.html', context)

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=user_name, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'login.html', context)



def LogoutPage(request):
    logout(request)
    return redirect('loginpage')



def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST' and request.FILES:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            gender = request.POST['gender']
            age = request.POST['age']
            email = request.POST['email']
            password = request.POST['password']
            profile = request.FILES.get('image')
            token = uuid.uuid4()
            
            user_obj = User(
                username=email, 
                first_name=firstname, 
                last_name=lastname, 
                email=email,
                date_joined=datetime.datetime.now())
            user_obj.set_password(password)
            user_obj.save()
            
            CreateUser.objects.create(
                user = user_obj,
                avatar=profile,
                user_uuid = str(token),
                age = age,
                user_gender = gender,
                email_token = str(token)
            )
            messages.success(request, 'Account created Successfully')
            send_verification_email(email, token)
            return redirect('loginpage')
        elif request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            gender = request.POST['gender']
            age = request.POST['age']
            email = request.POST['email']
            password = request.POST['password']
            token = uuid.uuid4()
            
            user_obj = User(
                username=email, 
                first_name=firstname, 
                last_name=lastname, 
                email=email,
                date_joined=datetime.datetime.now())
            user_obj.set_password(password)
            user_obj.save()
            
            CreateUser.objects.create(
                user = user_obj,
                user_uuid = str(token),
                age = age,
                user_gender = gender,
                email_token = str(token)
            )
            messages.success(request, 'Account created Successfully')
            send_verification_email(email, token)
            return redirect('loginpage')
            
        return render(request, 'signup.html', {})

def verify_email(request, token):
    try:
        user = CreateUser.objects.get(emil_token=token)
        user.is_verfied = True
        user.save() 
        return HttpResponse('email verfied successfully')
    except Exception:
        return HttpResponse('Invalid email token')
    
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def Dashboard(request):
    posts = AddPost.objects.all().order_by('-posted_time')

    context = {'posts': posts}
    return render(request, 'home.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def Profile(request):
    posts = AddPost.objects.filter(user_uuid = request.user.createuser)
    comments = Comment.objects.filter(user_uuid = request.user.createuser)
    context = {'posts': posts, 'comments': comments}
    return render(request, 'profile.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def Myposts(request):
    posts = AddPost.objects.filter(user_uuid = request.user.createuser).order_by('-posted_time')
    context = {'posts': posts}
    return render(request, 'myposts.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def Post(request):
    if request.method == 'POST' and request.FILES:
        title = request.POST['title']
        realese = request.POST['daterealesed']
        actors = request.POST['actors']
        genre = request.POST['genre']
        description = request.POST['description']
        link = request.POST['trailerlink']
        movie_flyer = request.FILES['movieposter']

        if len(link) == 0:
            AddPost.objects.create(
                user_uuid = request.user.createuser,
                title = title,
                release_date = realese,
                main_actors = actors,
                genre = genre,
                description = description,
                poster = movie_flyer,
                movie_trailer = "www.youtube.com",
                posted_time = datetime.datetime.now()
                )
        else:
            AddPost.objects.create(
                user_uuid = request.user.createuser,
                title = title,
                release_date = realese,
                main_actors = actors,
                genre = genre,
                description = description,
                poster = movie_flyer,
                movie_trailer = link,
                posted_time = datetime.datetime.now()

                )

        return redirect('dashboard')
    elif request.method == 'POST':
        title = request.POST['title']
        realese = request.POST['daterealesed']
        actors = request.POST['actors']
        genre = request.POST['genre']
        description = request.POST['description']
        link = request.POST['trailerlink']

        if len(link) == 0:
            AddPost.objects.create(
                user_uuid = request.user.createuser,
                title = title,
                release_date = realese,
                main_actors = actors,
                genre = genre,
                description = description,
                movie_trailer = "www.youtube.com",
                posted_time = datetime.datetime.now()
                )
        else: 

            AddPost.objects.create(
                user_uuid = request.user.createuser,
                title = title,
                release_date = realese,
                main_actors = actors,
                genre = genre,
                description = description,
                movie_trailer = link,
                posted_time = datetime.datetime.now()

                )

        return redirect('dashboard')



    return render(request, "post.html")





@login_required(login_url='loginpage')
def Update_Profile(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        user = User.objects.get(username=request.user.username)

        user.first_name = firstname
        user.last_name = lastname
        user.save()

        return redirect("profile")



@login_required(login_url='loginpage')
def Update_Picture(request):
    if request.method == 'POST' and request.FILES:
        user = User.objects.get(username=request.user.username)
        our_user = CreateUser.objects.get(user=user)
        image = request.FILES['img']
        our_user.avatar = image
        our_user.save()
        return redirect("profile")

    return redirect("profile")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def CommentPost(request, id):
    if request.method == 'POST':
        user = request.user.createuser
        post = id 
        message = request.POST['message']
        posted = datetime.datetime.now()


        new_comment = Comment(
            user_uuid = user,
            post = post,
            message = message,
            posted = posted
            )
        new_comment.save()

    post = AddPost.objects.get(pk=id)
    comments = Comment.objects.filter(post=id).order_by("-posted")
    context = {'post': post, 'comments': comments}

    return render(request, 'comment.html', context)



@login_required(login_url='loginpage')
def DeletePost(request, id):
    post = AddPost.objects.get(pk=id)
    if post.user_uuid.user_uuid != request.user.createuser.user_uuid:
            messages.info(request, "You can't delete that post, it doesn't belongs to You")
            return redirect('myposts')
    else:
        post.delete()
        messages.info(request, 'post delete successfully')
        return redirect('myposts')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def EditPost(request, id):
    post = AddPost.objects.get(pk=id)
    context = {'post': post}

    if request.method == 'POST':
        if post.user_uuid.user_uuid != request.user.createuser.user_uuid:
            messages.info(request, "You can't edit that post, it doesn't belongs to You")
            return redirect('myposts')
        else:
            new_title = request.POST['title']
            new_realese = request.POST['daterealesed']
            new_actors = request.POST['actors']
            new_genre = request.POST['genre']
            new_description = request.POST['description']
            new_link = request.POST['trailerlink']

            if len(new_link) == 0:
                post.title = new_title
                post.release_date = new_realese
                post.main_actors = new_actors
                post.genre = new_genre
                post.description = new_description
                post.movie_trailer = "www.youtube.com"
                post.posted_time = datetime.datetime.now()
                post.save()
                return redirect("myposts")
            else:
                post.title = new_title
                post.release_date = new_realese
                post.main_actors = new_actors
                post.genre = new_genre
                post.description = new_description
                post.movie_trailer = new_link
                post.posted_time = datetime.datetime.now()
                post.save()
                return redirect("myposts")

    elif request.method == 'POST' and request.FILES:
        if post.user_uuid.user_uuid != request.user.createuser.user_uuid:
            messages.info(request, "You can't edit that post, it doesn't belongs to You")
            return redirect('myposts')
        else:
            new_title = request.POST['title']
            new_realese = request.POST['daterealesed']
            new_actors = request.POST['actors']
            new_genre = request.POST['genre']
            new_description = request.POST['description']
            new_link = request.POST['trailerlink']
            new_movie_flyer = request.FILES['movieposter']

            def setpic(img):
                recent_pic = post.poster.path
                if os.path.exists(recent_pic):
                    os.remove
                return img


            if len(new_link) == 0:
                post.title = new_title
                post.release_date = new_realese
                post.main_actors = new_actors
                post.genre = new_genre
                post.description = new_description
                post.movie_trailer = "www.youtube.com"
                post.poster = setpic(new_movie_flyer)
                post.posted_time = datetime.datetime.now()
                post.save()
                return redirect("myposts")
            else:
                post.title = new_title
                post.release_date = new_realese
                post.main_actors = new_actors
                post.genre = new_genre
                post.description = new_description
                post.movie_trailer = new_link  
                post.poster = setpic(new_movie_flyer)
                post.posted_time = datetime.datetime.now()
                post.save()
                return redirect("myposts")

    return render(request, 'editpost.html', context)




@login_required(login_url='loginpage')
def Update_Pic(request, id):
    if request.method == 'POST' and request.FILES:
        post = AddPost.objects.get(pk=id)
        image = request.FILES['postimg']
        post.poster = image
        post.save()
        return redirect("myposts")

    return redirect("myposts")
