from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("messages/", views.inbox, name="inbox"),
    path("messages/start/<str:username>/", views.start_dm, name="start_dm"),
    path("messages/<int:convo_id>/", views.thread, name="thread"),
]
