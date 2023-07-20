from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from django.http import JsonResponse
from .utils.validMoves import get_valid_moves

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
    

class ValidMovesTestCase(TestCase):
    def test_get_valid_moves(self):
        board={"Queen": "E7", "Bishop": "B7", "Rook":"G5","Knight":"C3"}
        slug="Knight"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["B1","D1","A4","A2"])
        self.assertSetEqual(output_set,expected_output_set)

