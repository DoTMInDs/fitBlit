from django.shortcuts import render,redirect,get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required

from .models import PostModel,ArticlePostModel,Item
from core.models import Song,Artist
from.forms import CommentForm,ArticleCommentForm
from django.db.models import Q

from django.core.paginator import Paginator

def HomePageView(request):
    posts = PostModel.objects.all()
    articles = ArticlePostModel.objects.all()
    songs = Song.objects.all()
    items = Item.objects.all()
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    articles = ArticlePostModel.objects.filter(
        Q(title__icontains=filter_query) |
        Q(author__username__icontains=filter_query) |
        Q(sub_title__icontains=filter_query) |
        Q(article_content__icontains=filter_query)
    )
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    items = Item.objects.filter(
        Q(title__icontains=filter_query) |
        Q(location__icontains=filter_query) 
    )
    
    
    # # Pagination for articles
    # article_paginator = Paginator(articles, 5)  # Show 5 articles per page
    # article_page_number = request.GET.get('article_page')
    # article_page_obj = article_paginator.get_page(article_page_number)

   
    context = {
        'articles': articles,
        'posts': posts,
        'songs': songs,
        'items': items,
    }
    return render(request, 'home.html', context)

@login_required
def all_items(request):
    items = Item.objects.filter()

    context = {
        "items": items,
    }
    return render(request, 'all-details/all-items.html', context)


@login_required
def all_songs(request):
    songs = Song.objects.filter()

    context = {
        "songs": songs,
    }
    return render(request, 'all-details/artist-songs.html', context)

@login_required
def post_detail(request, pk):
    articles = ArticlePostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = ArticleCommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.article = articles
            instance.save()
            return redirect('blog-post-detail', pk=articles.id)
    else:
        c_form = ArticleCommentForm()
    context = {
        'articles': articles,
        'c_form': c_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def postmodel_detail(request, pk):
    post_mod = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.post_user = request.user
            instance.post_com = post_mod
            instance.save()
            return redirect('blog-postmodel-detail', pk=post_mod.id)
    else:
        c_form = CommentForm()
    context = {
        'post_mod': post_mod,
        'c_form': c_form,
    }
    return render(request, 'blog/postmodel_detail.html', context)
