
from django.urls import path
from .views import PositionView
urlpatterns = [
    #represents /chess/slug route. Handled by PositionView to calculate valid_positions 
    path('<str:slug>/', PositionView.as_view(),name="valid_positions"),
]