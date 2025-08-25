from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'news'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),
    
    # Article URLs
    path('article/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Category URLs
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category_detail'),
    
    # Tag URLs
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Comment
    path('add-comment/<int:article_id>/', views.AddCommentView.as_view(), name='add_comment'),
]