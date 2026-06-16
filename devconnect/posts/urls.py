from django.urls import path

from . import views


urlpatterns = [

    path('',
         views.post_list,
         name='post_list'),

    path('create/',
         views.post_create,
         name='post_create'),

    path('<int:id>/share/',
     views.post_share,
     name='post_share'),

    path('<int:id>/',
         views.post_detail,
         name='post_detail'),

    path('<int:id>/edit/',
         views.post_update,
         name='post_update'),

    path('<int:id>/delete/',
         views.post_delete,
         name='post_delete'),
     
     path('search/',
     views.post_search,
     name='post_search'),

     path('<int:id>/like/',
     views.post_like,
     name='post_like'),
]