from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import UserModel, Song, Watchlater, History, Channel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from SocialMe import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.db.models import Case, When
from datetime import date
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def home(request):
    temp_song = {}
    temp_song_name = Song.objects.all().values_list('name')
    song_name = []
    for i in temp_song_name:
        song_name.append(i[0])
    
    temp_song_singer = Song.objects.all().values_list('singer')
    song_singer = []
    for i in temp_song_singer:
        song_singer.append(i[0])

    temp_song_song = Song.objects.all().values_list('song')
    song_song = []
    for i in temp_song_song:
        song_song.append(i[0])

    temp_song_id = Song.objects.all().values_list('song_id')
    song_id = []
    for i in temp_song_id:
        song_id.append(i[0])

    song_number = []
    for i in range(0,len(song_name)):
        song_number.append("_" + str(i+1))

    temp_song['name'] = song_name
    temp_song['singer'] = song_singer
    temp_song['song'] = song_song
    temp_song['id'] = song_id
    temp_song['number'] = song_number
    print(temp_song)

    json_object = json.dumps(temp_song, indent = 4)
    with open("static/js/data.json", "w") as outfile:
        outfile.write(json_object)
    


    song = Song.objects.all()[0:3]



    if request.user.is_authenticated:
        myuser = UserModel.objects.get(id=request.user.id)
        wl = Watchlater.objects.filter(user=myuser)
        ids = []
        for i in wl:
            ids.append(i.video_id)
        
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved) 
        watch = reversed(watch)
    
    else:
        watch = Song.objects.all()[0:3]

    if request.POST.get('bday',False):
        bday = request.POST.get('bday',False)
        state = request.POST.get('state',False)
        city = request.POST.get('city',False)
        number = request.POST.get('number',False)
        profile_image = request.FILES['profile_image']
        plan = request.POST['plan']

        myuser = UserModel.objects.get(first_name=request.user.first_name)
        myuser.birth_date = bday
        myuser.state = state
        myuser.city = city
        myuser.number = number
        myuser.profile_image = profile_image
        myuser.plan = plan
        myuser.is_updated = True
        myuser.save()
        return render(request, 'index.html',{"myuser":myuser})
    else:     
        if request.user.is_authenticated:
            myuser = UserModel.objects.get(username=request.user.username)
            return render(request, 'index.html',{"myuser":myuser, 'song': song, 'watch': watch})
        
        else:
            return render(request, 'index.html', {'song': song, 'watch': watch})

def signup(request):

    if request.method == "POST":
            # myuser = User.objects.get(first_name=fname)
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print("Hello!! I am here")

        if UserModel.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if UserModel.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum(): 
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = UserModel.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        

        myuser.save()

        channel = Channel.objects.create(name=username)
        channel.save()

        messages.success(request,"Your accunt is successfully created!!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to KYM System!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to KYM System!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Developer Team"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email] # Can i send bulk mails?
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('User/email_confirmation.html',{
            
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send() 

        return redirect('signin')

    return render(request, 'User/signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['passwordlogin']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            myuser = UserModel.objects.get(username=username)
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, 'User/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = UserModel.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        logout(request)
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

@login_required(login_url='signin')
def add_detail(request):
    print(request.user)
    if request.user.is_authenticated:
        myuser = UserModel.objects.get(id=request.user.id)
        return render(request,'User/add_detail.html',{"myuser":myuser})
    else:
        return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    if request.user.is_authenticated and not request.POST.get('id'):
        if request.user.is_authenticated and request.POST.get('current_password',False):
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            myuser = UserModel.objects.get(id=request.user.id)
            if myuser.check_password(current_password):
                if new_password != confirm_password:
                    messages.error(request, "Confirm password should be same as new password")
                    return redirect('profile')
                else:
                    myuser.set_password(new_password)
                    myuser.save()
                    return redirect('signin')
            else:
                messages.error(request, "Enter currect password")
                return redirect('profile')

        else:
            myuser = UserModel.objects.get(id=request.user.id)
            return render(request,'User/profile.html',{"myuser":myuser})
    elif request.user.is_authenticated and request.POST.get('id'):
        p_id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        plan = request.POST.get('plan')
        
        city = request.POST.get('city')
        # print(request.FILES['profile_image'])
        myuser = UserModel.objects.get(id=p_id)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.plan = plan

        if(request.FILES.get('profile_image', False)):
            profile_image = request.FILES['profile_image']
            myuser.profile_image.storage.delete(myuser.profile_image.name)
            myuser.profile_image = profile_image
        
        if(request.POST.get('state', False)):
            state = request.POST.get('state')
            myuser.state = state

        if(request.POST.get('city', False)):
            city = request.POST.get('city')
            myuser.city = city
        # myuser.profile_image = profile_image
        
        myuser.save()
        return render(request,'User/profile.html',{"myuser":myuser})
    
    else:
        return redirect('signin')

def history(request):
    myuser = UserModel.objects.get(id=request.user.id)

    if request.method == "POST":
        user = request.user
        myuser = UserModel.objects.get(id=request.user.id)
        music_id = request.POST['music_id']
        history = History(user=myuser, music_id=music_id)
        history.save()

        return redirect(f"/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'musicbeats/history.html', {"history": song,"myuser":myuser})

def watchlater(request):
    myuser = UserModel.objects.get(id=request.user.id)
    if request.method == "POST":
        myuser = UserModel.objects.get(id=request.user.id)
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=myuser)
        
        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=myuser, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"musicbeats/songpost.html", {'song': song, "message": message, "myuser":myuser})

    wl = Watchlater.objects.filter(user=myuser)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "musicbeats/watchlater.html", {'song': song,"myuser":myuser})

def songs(request):
    if request.user.is_authenticated:
        song = Song.objects.all()
        myuser = UserModel.objects.get(id=request.user.id)
        return render(request, 'musicbeats/songs.html', {'song': song,"myuser":myuser})


    song = Song.objects.all()
    return render(request, 'musicbeats/songs.html', {'song': song})

def songpost(request, id):
    mysong = Song.objects.all()
    stuff = get_object_or_404(Song , song_id=id)
    likes = stuff.total_likes()
    if request.user.is_authenticated:
        myuser = UserModel.objects.get(id=request.user.id)
        song = Song.objects.filter(song_id=id).first()
        return render(request, 'musicbeats/songpost.html', {'song': song,"myuser":myuser, "mysong":mysong, 'likes':likes})    

    song = Song.objects.filter(song_id=id).first()
    return render(request, 'musicbeats/songpost.html', {'song': song , "mysong":mysong, 'likes':likes})

def channel(request, channel):
    myuser = UserModel.objects.get(id=request.user.id)
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "musicbeats/channel.html", {"channel": chan, "song": song,"myuser":myuser})

def upload(request):
    myuser = UserModel.objects.get(id=request.user.id)
    if request.method == "POST":
        
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        image = request.FILES['image']
        movie = request.POST['movie']
        credit = request.POST['credit']
        song1 = request.FILES['file']

        song_model = Song(user=myuser,name=name, singer=singer, tags=tag, image=image, movie=movie, credit=credit, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find) 

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()
        return redirect('home')
    return render(request, "musicbeats/upload.html",{'myuser':myuser})
        
def like_view(request,pk):
    id = request.POST.get('song_id')
    song = Song.objects.get(song_id = id)
    song.like.add(request.user)
    
    return HttpResponseRedirect(reverse('songpost',args=[str(pk)]))


def delete_song(request,pk):
    song_to_delete=Song.objects.get(song_id=pk)
    song_to_delete.delete()
    return redirect('home')