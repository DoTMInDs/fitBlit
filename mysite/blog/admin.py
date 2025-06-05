from django.contrib import admin
from .models import Profile,Author,Item,ItemImage,PostModel,ArticlePostModel,PostComment,ArticleComment
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display=['fullname','phone','email']
    readonly_fields=['fullname','phone','email']

# Register your models here.
admin.site.register(Profile,ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Author)
admin.site.register(PostModel)
admin.site.register(ArticlePostModel)
admin.site.register(PostComment)
admin.site.register(ArticleComment)
admin.site.register(Item)
admin.site.register(ItemImage)
