from django.contrib.sitemaps.views import index
from django.urls import path
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from job import views
from django.views.generic.base import RedirectView
from django.conf.urls import url
from . import views

urlpatterns=[

    #path('index/', views.index),

    path('add_student/', views.add_student),
    path('add_teacher/', views.add_teacher),
    path('add_course/', views.add_course),
    path('publish_notice/', views.publish_notice),
    path('modify_student/', views.modify_student),
    path('modify_teacher/', views.modify_teacher),
    path('modify_course/', views.modify_course),
    path('delete_student/', views.delete_student),
    path('delete_teacher/', views.delete_teacher),
    path('delete_course/', views.delete_course),
    path('modify_homework/', views.modify_homework),
    path('modify_sign/', views.modify_sign),
    path('delete_homework/', views.delete_homework),
    path('delete_sign/', views.delete_sign),
    path('publishsign/', views.publishsign),
    path('Sign/', views.Sign),
    path('GetSign/', views.GetSign),
    path('stuchangepasswork/', views.stuchangepasswork),
    path('teachangepasswork/', views.teachangepasswork),
    path('machangepasswork/', views.machangepasswork)


    #path('is_admin/', views.is_admin),
]