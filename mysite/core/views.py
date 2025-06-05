from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from blog.models import PostModel,ArticlePostModel
from blog.forms import CommentForm,ArticleCommentForm,ArtistPostForm,AlbumForm,SongUploadForm
from django.db.models import Q
from .models import Artist,Album,SportsModel,Song
from blog.models import Item,ItemImage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import ItemForm,ItemEditForm,ItemImageFormSet
# from django.contrib import messages

# import requests
# import logging
# from django.conf import settings

# from .forms import PaymentForm
# from .models import Payment

# logger = logging.getLogger(__name__)


@login_required
def NewsPage(request):
    posts = PostModel.objects.all()
    articles = ArticlePostModel.objects.all()
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    articles = ArticlePostModel.objects.filter(
        Q(title__icontains=filter_query) |
        Q(author__username__icontains=filter_query) |
        Q(sub_title__icontains=filter_query) 
    )
    
     # Pagination for articles
    article_paginator = Paginator(articles, 5)  # Show 5 articles per page
    article_page_number = request.GET.get('article_page')
    article_page_obj = article_paginator.get_page(article_page_number)

    context = {
        # 'articles': articles,
        'article_page_obj': article_page_obj,
        'posts': posts,
    }
    return render(request, 'core/news.html', context)

def SportsPage(request):
    posts = SportsModel.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'core/sports.html',context)

@login_required
def  BusinessPage(request):
    items = Item.objects.all()
    form = ItemForm()
    image_formset = ItemImageFormSet(queryset=ItemImage.objects.none())
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    items = Item.objects.filter(
        Q(title__icontains=filter_query) |
        Q(location__icontains=filter_query) |
        Q(description__icontains=filter_query) 
    )
    
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        image_formset = ItemImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and image_formset.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            
            for image_form in image_formset:
                image = image_form.save(commit=False)
                image.item = item
                image.save()
            
            messages.success(request, 'Item created successfully!')
            return redirect('business-page')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    context = {
        "items": items,
        "form": form,
        'image_formset': image_formset,
    }
    return render(request, 'core/business.html',context)

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    images = item.images.exclude(image__isnull=True)
    # e_form = ItemEditForm()
    # image_form = ItemImageFormSet()

    if request.method == "POST":
        e_form = ItemEditForm(request.POST, request.FILES, instance=item)
        image_form = ItemImageFormSet(request.POST, request.FILES, queryset=item.images.all())

        if e_form.is_valid() and image_form.is_valid():
            e_form.save()
            images = image_form.save(commit=False)
            for image in images:
                image.item = item 
                image.save()
            for deleted_image in image_form.deleted_objects:
                deleted_image.delete()
            messages.success(request, 'Item and images updated successfully!')
            return redirect('item-detail', pk=item.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        e_form = ItemEditForm(instance=item)
        image_form = ItemImageFormSet(queryset=item.images.all())

    context = {
        "item": item,
        "e_form": e_form,
        "image_form": image_form,
        "images": images,
    }
    return render(request, "all-details/item-detail.html", context)

@login_required
def delete_item(request, pk):
    items = Item.objects.get(id=pk)
    if request.method == 'POST':
        items.delete()
        return redirect('business-page')
    context = {
        'items': items,
    }
    return render(request, 'all-details/delete_item.html', context)

def OpinionsPage(request):
    return render(request, 'core/opinions.html')

def GhanawebPage(request):
    return render(request, 'core/ghanaweb.html')

@login_required
def MusicPage(request):
    query = request.GET.get('search', '')
    if query:
        artist_uploads = Artist.objects.filter(Q(artist__icontains=query) | Q(artist_genre__icontains=query))
        albums = Album.objects.filter(Q(title__icontains=query) | Q(artist__artist__icontains=query))
    else:
        artist_uploads = Artist.objects.all()
        albums = Album.objects.all()
    
    form = ArtistPostForm()   
    a_form = AlbumForm() 

    if request.method == "POST":
        if 'form' in request.POST:
            form = ArtistPostForm(request.POST, request.FILES)        
            if form.is_valid() :
                artist = form.save(commit=False)
                artist.user = request.user
                artist.save()            
                return redirect('music-page')
        elif 'a_form' in request.POST:
            a_form = AlbumForm(request.POST, request.FILES)
            if a_form.is_valid():
                album = a_form.save(commit=False)
                album.user = request.user
                album.save()
                return redirect('music-page')
        
    else:
        form = ArtistPostForm()
        a_form = AlbumForm() 

    context = {
        "artist_uploads": artist_uploads,
        "albums": albums,
        "form": form,
        "a_form": a_form,
        
    }
    return render(request, 'core/music.html', context)

def AfricaPage(request):
    return render(request, 'core/africa.html')

@login_required
def ArtistDetailPage(request, artist_id):
    artist_uploads = get_object_or_404(Artist, id=artist_id)
    songs = Song.objects.filter(artist=artist_uploads)
    song_form = SongUploadForm()
    
    if request.method == "POST" and 'song_form' in request.POST:
        song_form = SongUploadForm(request.POST, request.FILES)
        if song_form.is_valid():
            song = song_form.save(commit=False)
            song.artist = artist_uploads
            song.user = request.user
            song.save()
            return redirect('artist-detail', artist_id=artist_uploads.id)

    context = {
        "artist_uploads": artist_uploads,
        "songs": songs,
        'song_form': song_form,
    }
    return render(request, 'artists/artist_detail.html', context)


@login_required
def all_artist(request):    
    artist_uploads = Artist.objects.all()
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    artist_uploads = Artist.objects.filter(
        Q(artist__icontains=filter_query) |
        Q(artist_genre__icontains=filter_query)
    )

    context = {
        "artist_uploads": artist_uploads,
    }
    return render(request, 'artists/all_artist.html', context)
    
@login_required
def all_album(request):
    albums = Album.objects.all()
    
    filter_query = request.GET.get('search') if request.GET.get('search') != None else ''
    albums = Album.objects.filter(
        Q(artist__artist__icontains=filter_query) |
        Q(title__icontains=filter_query)
    )

    context = {
        "albums": albums,
    }
    return render(request, 'artists/all_album.html', context)

@login_required
def AlbumDetail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    song_form = SongUploadForm()
    
    if request.method == "POST":
        if 'song_form' in request.POST:
            song_form = SongUploadForm(request.POST, request.FILES)
            if song_form.is_valid():
                song = song_form.save(commit=False)
                song.album = album
                song.artist = album.artist
                song.save()
                return redirect('album-detail', album_id=album.id)
    else:
        song_form = SongUploadForm()

    context = {
        "album": album,
        "song_form": song_form,
        'songs': album.songs.all(),
    }
    return render(request, 'artists/album_details.html', context)
    

def SportDetailPage(request, pk):
    posts = SportsModel.objects.get(id=pk)
    post_mod = PostModel.objects.get(id=pk)

    context = {
        'posts': posts,
        'post_mod': post_mod,
    }
    return render(request, 'artists/sport_detail.html', context)


