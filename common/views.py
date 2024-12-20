from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm


def signup(request):            #계정생성
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


#404 Page not found, 
# settings.py 
# DEBUG=False 
# ALLOWED_HOSTS = ['127.0.0.1']
def page_not_found(request, exception):     
    return render(request, 'common/404.html')
