from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('register/', views.register,
         name='register'),

    path('edit/', views.edit,
         name='edit'),

     path('users/<str:username>/',
     views.user_detail,
     name='user_detail'),

     path('follow/<str:username>/',
     views.user_follow,
     name='user_follow'),
]
