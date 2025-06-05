# from django.contrib.auth.models import User
from django import forms # type: ignore
from .models import PostComment,ArticleComment

from core.models import Artist,Album,Song

class CommentForm(forms.ModelForm):
    post_content = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Add comments here....'}))
    class Meta:
        model = PostComment
        fields = ("post_content",)

class ArticleCommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Add comments here....'}))
    class Meta:
        model = ArticleComment
        fields = ("content",)

class ArtistPostForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = (
            "artist", 
            "artist_genre", 
            "artist_image", 
            "artist_profile"
        )

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'genre', 'cover_image', 'song_file', 'album']

class AlbumForm(forms.ModelForm):
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), required=True, label="Select Artist")
    class Meta:
        model = Album
        fields = [
            "title", 
            "release_date", 
            "cover_image",
            "artist",
        ]
