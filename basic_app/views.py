from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

#built-in modules for the login functionality
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False 

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #for hashing the password.
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(
        request,
        'basic_app/registration.html',
        context={
            'user_form' :user_form,
            'profile_form' :profile_form,
            'registered' :registered
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('special'))
            
            else:
                return HttpResponse("Account isn't active")
            
        else:
            print('Login failed!!')
            print('UserName: {} and Password: {}'.format(username,password))
            return HttpResponse('Invalid login details..')
    else:
        return render(request,'basic_app/login.html')
    
@login_required
def special(request):
    #return HttpResponse('You are logged in!!')
    return render(request,'basic_app/special.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
        