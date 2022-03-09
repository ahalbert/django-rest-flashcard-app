from django.urls import path
from .views import appView

urlpatterns = [
    path('', appView, name='Flashcard App Client'),
]
