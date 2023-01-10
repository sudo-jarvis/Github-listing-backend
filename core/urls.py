from django.urls import path
from core import views

urlpatterns = [
    path('user/', views.UserClass.as_view()),
    path('user/repos', views.RepoClass.as_view()),
]
