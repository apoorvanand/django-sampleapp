from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [ 
    path('', views.index, name='index'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('search/', views.post_list, name='search'),


]