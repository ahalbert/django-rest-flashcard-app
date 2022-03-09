from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import generics
from django.views.generic import View
from rest_framework.decorators import api_view

from django.utils import timezone
from datetime import timedelta

from .models import Card
from .serializers import CardSerializer

buckets_to_timedeltas = [timedelta(seconds=0), timedelta(seconds=5), timedelta(seconds=25), timedelta(minutes=2), timedelta(minutes=5),
                         timedelta(minutes=10), timedelta(hours=1), timedelta(hours=5), timedelta(days=1), timedelta(days=5), timedelta(days=25),
                         timedelta(days=120)
                        ]
# Create your views here.

@api_view(['GET'])
def nextCard(request):
    anyCardsLeft = False
    for b in range(10,-1,-1):
        cards_in_bucket = Card.objects.filter(bucket=b)
        for card in cards_in_bucket:
            anyCardsLeft = True
            if card.dateNextReviewed < timezone.now() and card.numberOfTimesWrong < 10:
                seralizedCard = CardSerializer(card)
                return JsonResponse(seralizedCard.data, safe=False)
    if anyCardsLeft:
        return JsonResponse({"message": "cards temporarily done."})
    else:
        return JsonResponse({"message" : "all cards done."})

class AppView(View):
    model = Card
    template_name = 'index.html'

class ListCards(generics.ListCreateAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.all()

class DetailCard(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Card.objects.all() 
    serializer_class = CardSerializer

@api_view(['GET'])
def resetCards(request):
    Card.objects.all().update(bucket=0)
    return JsonResponse({})

@api_view(['POST'])
def reviewCard(request):
    card = Card.objects.get(pk=request.data['id'])
    if request.data['isCorrect'] == 'true':
        if card.bucket >= 10:
            card.bucket = 11
        else:
            card.bucket = card.bucket + 1
    else:
        card.bucket = 1
        card.numberOfTimesWrong = card.numberOfTimesWrong + 1
    card.dateNextReviewed = timezone.now() + buckets_to_timedeltas[card.bucket]
    card.save()
    return JsonResponse({})
