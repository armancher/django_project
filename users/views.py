from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from users.models import User


# Create your views here.
def user_register_view(request):
    if request.method == 'POST' :
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'you registered successfully')
            login_user=authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
            login(request,login_user)
            return redirect('users:home')
        else:
            messages.warning(request,'register unsuccessfully')
    else:
        form=UserRegisterForm()
    context={
        'form': form ,
        }
    return render(request,'user/user_register_form.html',context=context)


def user_login_view(request):
    if request.method == 'POST' :
        form=UserLoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'login successful')
                return redirect('users:home')
        messages.warning(request,'login unsuccessful') 
        
    else:
        form=UserLoginForm()
    context={
            'form': form ,
        }
    return render(request,'user/user_login_form.html',context=context)
                
            
           
    


def user_logout_view(request):
    logout(request)
    return redirect('users:login')


def user_profile_view(request, uid):
    user=get_object_or_404(User,id=uid)
    context={
        'user': user,
        'uid': uid ,
    }
    return render(request,'user/user_profile_view.html',context=context)

def user_profile_edit_view(request):
    
    if request.method=='POST':
        form=UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:home')
    else:
        form=UserUpdateForm(instance=request.user)
    context={
            'form': form ,
        }
    return render(request,'user/user_edit.html',context=context)


def user_home_view(request):
    return render(request, 'home.html')