
from django.urls import path
from .views import PositionView
urlpatterns = [
    path('', PositionView.as_view(),name="valid_positions"),
]
