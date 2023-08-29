from django.urls import path

from . import views

urlpatterns = [
     path('boardData', views.BoardData),
     path('docDetails/<str:id>', views.DocUpdate),
     path('docs', views.Docs)
]
