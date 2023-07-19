from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from django.http import JsonResponse

# Create your tests here.

class PositionTest(TestCase):
    def setUp(self):
        self.client=APIClient()
    
    def test_valid_positions(self):
        request_data={"positions": {"Queen": "D5", "Bishop": "H1", "Rook":"A1","Knight":"F3"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,200)
        expected_response_data={"valid_moves": ["G2"]}
        self.assertEqual(response.content,JsonResponse(expected_response_data).content)
