from django.urls import path
from Application import views

app_name = "fileapp"

urlpatterns = [
    path('', views.index),
    path("range-transcript", views.range_transcript, name = "range-transcript"),
    path("all-transcript", views.all_transcript, name = "all-transcript"),
]