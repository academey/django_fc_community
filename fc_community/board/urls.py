from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
]
