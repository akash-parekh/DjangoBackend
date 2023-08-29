from django.urls import path

from . import views

urlpatterns = [
     path('boardData', views.BoardData),
     path('docUpdate/<str:id>', views.DocUpdate),
]
