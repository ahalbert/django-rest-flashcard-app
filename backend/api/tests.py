from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient
import json

from .models import Card


class ApiTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        card1 = Card.objects.create(word="test", definition="this card should appear where card3 does not")
        card1.save()
        card2 = Card.objects.create(word="test never bucket", definition="This card should never be picked", bucket=11)
        card2.save()
        card3 = Card.objects.create(word="bucket 2", definition="This card should be next by default.", bucket=2)
        card3.save()


    def testCreate(self):
        card = Card.objects.get(id=1)
        self.assertEqual(card.bucket, 0)
        self.assertEqual(card.word, "test")
        self.assertEqual(card.definition, "this card should appear where card3 does not")

    def testGetNextCard(self):
        client = RequestsClient()
        response = client.get('http://localhost:8000/api/next/')
        data = json.loads(response.text)
        self.assertEqual(data['bucket'],2)
        self.assertEqual(data['word'],"bucket 2")
        self.assertEqual(data['definition'],"This card should be next by default.")

    def testWrongAnswer(self):
        client = RequestsClient()
        response = client.post('http://localhost:8000/api/review/', json={"isCorrect" : "false", "id" : 1})
        card = Card.objects.get(id=1)
        self.assertEqual(card.bucket, 1)

    def testRightAnswer(self):
        client = RequestsClient()
        response = client.post('http://localhost:8000/api/review/', json={"isCorrect": "true", "id": 3})
        card = Card.objects.get(id=3)
        self.assertEqual(card.bucket, 3)

    def testDateReviewPassed(self):
        client = RequestsClient()
        response = client.post('http://localhost:8000/api/review/', json={"isCorrect": "true", "id": 3})
        response = client.get('http://localhost:8000/api/next/')
        data = json.loads(response.text)
        self.assertEqual(data['id'], 1)

    def testExceededMaxWrongTries(self):
        client = RequestsClient()
        card = Card.objects.get(id=3)
        card.numberOfTimesWrong = 10
        card.save()
        response = client.get('http://localhost:8000/api/next/')
        data = json.loads(response.text)
        self.assertEqual(data['id'], 1)

    def testTemporarilyDone(self):
        client = RequestsClient()
        response = client.post('http://localhost:8000/api/review/', json={"isCorrect": "true", "id": 1})
        response = client.post('http://localhost:8000/api/review/', json={"isCorrect": "true", "id": 3})
        response = client.get('http://localhost:8000/api/next/')
        data = json.loads(response.text)
        self.assertEqual(data['message'], 'cards temporarily done.')

    def testAllDone(self):
        client = RequestsClient()
        Card.objects.all().update(bucket=11)
        response = client.get('http://localhost:8000/api/next/')
        data = json.loads(response.text)
        self.assertEqual(data['message'], "all cards done.")
