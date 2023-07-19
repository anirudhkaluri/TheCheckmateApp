
from django.urls import path
from .views import PositionView
urlpatterns = [
    path('<str:slug>/', PositionView.as_view(),name="valid_positions"),
]