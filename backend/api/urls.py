from django.urls import path
from .views import ListCards, DetailCard, nextCard, reviewCard, resetCards

urlpatterns = [
    path('<int:pk>/', DetailCard.as_view()),
    path('', ListCards.as_view()),
    path('next/', nextCard),
    path('review/',reviewCard),
    path('reset/', resetCards),

]
