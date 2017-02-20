from django.shortcuts import render
from .models import Article,Comment,Poll,NewUser
from .forms import CommentForm,LoginForm,RegisterForm,SetInfoForm,SearchForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

import markdown2
# from urlparse import urlparse   py3中没有urlparse
from urllib import parse
# Create your views here


def index(request):
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    context = {'latest_article_list':latest_article_list,'loginform':loginform}
    return render(request, 'index.html',context)

def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html',{'form':form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                url = request.POST.get('source_url','/focus')
                return redirect(url)
            else:
                return render(request, 'login.html',{'form':form,'error':'Password or username is incorrect, pls confirm it!'})
        else:
            return render(request, 'login.html',{'form':form})

@login_required
def log_out(request):
    url = request.POST.get('source_url','/focus/')
    logout(request)
    return redirect(url)
# @login_required这个装饰器是django内置的,它的作用是使所装饰的函数必须是登录的用户才继续运行，不然进入指定的login_url,
# 我们这里没有指定login_url，所以在settings.py中添加以下代码：
# LOGIN_URL = "/focus/login/?next='article_id'"
# next表示登录后自动进入的页面。