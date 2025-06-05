from django.urls import path
# from .views import AboutPageView
# from .views import SearchPageView
# from .views import CategoriesPageView
# from .views import ContactPageView
from . import views


urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('all_songs/', views.all_songs, name='all-songs'),
    path('all_items/', views.all_items, name='all-items'),
    
    path('post_detail/<int:pk>/', views.post_detail, name='blog-post-detail'),
    path('postmodel_detail/<int:pk>/', views.postmodel_detail, name='blog-postmodel-detail'),
]

