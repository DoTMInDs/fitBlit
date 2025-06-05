# from django.forms import ModelForm
from typing import Any
from django import forms # type: ignore
from .models import ProfileModel
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from cloudinary.forms import CloudinaryFileField

from blog.models import ArticlePostModel


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your username....'}))
    email = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your email....'}))
    password1 = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your password....'}))
    password2 = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Confirm your password....'}))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args: Any, **kwargs: Any):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].help_text = None 


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your username....'}))
    email = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your email....'}))
    class Meta:
        model = User
        fields = [ "username", "email"]
    def __init__(self, *args: Any, **kwargs: Any):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for fieldname in [ "username", "email"]:
            self.fields[fieldname].help_text = None

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your fullname....'}))
    about = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Tell us something about you....'}))
    talks_about = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Type something here....'}))
    class Meta:
        model = ProfileModel
        fields = [ "full_name", "image", "about", "talks_about"]

class UserPostForm(forms.ModelForm):
    article_content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = ArticlePostModel
        fields = ("title", "sub_title", "article_content", "image", "slug")

class PostEditForm(forms.ModelForm):
    article_content = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))
    slug = forms.SlugField(required=False)
   
    class Meta:
        model = ArticlePostModel
        fields = ("title", "article_content", "image", "slug")
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not hasattr(image, 'name'):
            image.name = 'temp.jpg'
        return image
