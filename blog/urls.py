from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('my-posts/', views.MyPostsView.as_view(), name='my_posts'),
    path('category/<slug:slug>/', views.CategoryPostView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagPostView.as_view(), name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
