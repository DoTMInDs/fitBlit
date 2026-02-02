from django.shortcuts import render,redirect, get_object_or_404 # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Q
from django.core.paginator import Paginator

from blog.models import ArticlePostModel
from .models import ProfileModel
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm,UserPostForm,PostEditForm




# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please input a valid username and password")
       
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
    

def reset_password(request):
    return render(request, 'users/reset_password.html')


def sign_up(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.set_password(form.cleaned_data.get('password1'))
            user.save()

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Please input a valid username and password")
       
    context = {'form':form}
    return render(request, 'users/sign_up.html', context)

@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(ProfileModel, user=user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST or None, instance=user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def user_dashboard(request):
    articles = ArticlePostModel.objects.all()
    user_post_form = UserPostForm()

    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    articles = ArticlePostModel.objects.filter(
        Q(title__icontains=filter_query) |
        Q(author__username__icontains=filter_query) |
        Q(sub_title__icontains=filter_query) 
    )
    
    # Pagination for articles
    article_paginator = Paginator(articles, 25)  # Show 5 articles per page
    article_page_number = request.GET.get('article_page')
    article_page_obj = article_paginator.get_page(article_page_number)

    if request.method == "POST":
        user_post_form = UserPostForm(request.POST, request.FILES)
        if user_post_form.is_valid():
            instance = user_post_form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('user-dashboard')
        else:
            print(user_post_form.errors)
            print('there is an error somewhere')
            user_post_form = UserPostForm()
    context = {
        # 'articles': articles,
        'article_page_obj': article_page_obj,
        'user_post_form': user_post_form,
    }
    return render(request, 'dashboard/dashboard.html',context)

@login_required
def user_dashboard_edit(request, pk):
    article = get_object_or_404(ArticlePostModel, id=pk)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            # Handle file uploads specifically for Cloudinary
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                if not hasattr(image_file, 'name'):
                    image_file.name = 'temp.jpg'  # Or any fake name with correct extension
                form.instance.image = image_file
            form.save()
            messages.success(request, 'post updated successfully!')
            return redirect('user-dashboard')
        else:
            for error in form.errors:
                print("Form error:", error, form.errors[error])
    else:
        form = PostEditForm(instance=article)
   
    context = {
        'articles': article,
        'form': form,
    }
    return render(request, 'dashboard/user_dashboard_edit.html', context)

@login_required
def user_post_delete(request, pk):
    articles = ArticlePostModel.objects.get(id=pk)

    if request.method == 'POST':
        articles.delete()
        messages.success(request, 'post deleted successfully!')
        return redirect('user-dashboard')
    return redirect('user-dashboard')