from django.urls import path
from . import views

urlpatterns = [
    path('recommender/', views.recommender),
    path('detail/', views.detail),
]
