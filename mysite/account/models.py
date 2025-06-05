from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import FileExtensionValidator # type: ignore
from cloudinary.models import CloudinaryField

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = CloudinaryField('image', folder='profile_pics',null=True ,blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])
    full_name = models.CharField(null=True,max_length=200)
    about = models.TextField(null=True)
    talks_about = models.CharField(max_length=255, default='anything', null=True)

    def __str__(self):
        return f'Profile of {self.about}'

class UserPostModel(models.Model):
    title=models.CharField(max_length=200, unique=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post_content=models.TextField()

    def __str__(self):
        return self.title
    