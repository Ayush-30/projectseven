from django.shortcuts import render, redirect
from django.contrib import messages
from .form import createuserform
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email,ValidationError

def base(request):
    return render(request, 'user/base.html')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['uname']
        # email = request.POST['email']
        password = request.POST['psw']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'invalid')
            return redirect('login')

    else:
        return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'user already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken ......')
                return redirect('register')
            else:

                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save();

                messages.success(request, 'user created')
                return redirect('dashboard')

        else:
            messages.info(request, 'password not match...')
            return redirect('register')


    else:
        return render(request, 'user/register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

# def register1(request):
#     if request.method == 'POST':
#         form = createuserform(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created ,please login with your account {username}!')
#             return redirect('dashboard')
#     else:
#         form = createuserform()
#     return render(request, 'user/register1.html', {'form': form})
# Create your views here.
