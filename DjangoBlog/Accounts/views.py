from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .forms import SignUpForm,LoginForm

# Create your views here.
def signup_view(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            login(request,user)
            return redirect('article:list')
    else:
        form=SignUpForm()
        print(form)
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form = LoginForm(data=request.POST)    
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('article:list')
    else:

        form=LoginForm()
    return render(request,'login.html',{'form':form})

def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('article:list')


