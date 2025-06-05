from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
# from blog.models import Author

# Create your models here.
class ArtistName(models.Model):
    name_of_artist=models.CharField(max_length=100,null=True,unique=True)
    def __str__(self) -> str:
        return self.name_of_artist

class Artist(models.Model):        
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    artist = models.CharField(max_length=200, null=True,unique=True)
    artist_genre = models.CharField(max_length=200,null=True)
    artist_image=CloudinaryField('image', folder='artist_cover',null=True,blank=True,validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])
    artist_profile=CloudinaryField('image', folder='artist_profile',null=True,blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])
    posted_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return str(self.artist)
    
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    cover_image = CloudinaryField('image', folder='album_cover', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return f'{self.title} - {self.artist} - released on - {self.release_date}'
    
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs', null=True,blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, null=True)
    cover_image = CloudinaryField('image', folder='song_cover', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])
    song_file = models.FileField(upload_to='music', null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
   
    
class SportsModel(models.Model):
    title=models.CharField(max_length=200, unique=True)
    sub_title=models.CharField(max_length=200, unique=True,null=True)
    artist_song_create = models.FileField(upload_to='video/',null=True,blank=True, validators=[FileExtensionValidator(['MOV', 'WMV', 'MP4', 'FLV', 'WEBM', 'AVI', 'MKV'])])
    # image=CloudinaryField(upload_to='images/',null=True,blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug=models.SlugField(max_length=200, unique=True)
    article_content=models.TextField(null=True)
    dated_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-dated_on',)

    def __str__(self):
        return self.title
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    momo_transaction_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"