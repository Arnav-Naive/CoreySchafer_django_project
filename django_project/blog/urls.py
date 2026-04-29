from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),        # <int:pk> means that we are expecting an integer value for the primary key of the post, and we will pass that value to the PostDetailView
    path('post/new/', PostCreateView.as_view(), name='post-create'),             #it will share template with update-view
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
    path('about/', views.about, name='blog-about'),
]

