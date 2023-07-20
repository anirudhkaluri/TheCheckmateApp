from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from rest_framework.exceptions import ErrorDetail
from django.http import JsonResponse
from .utils.validMoves import get_valid_moves
from .serializers import PositionSerializer

# Create your tests here.


class PositionSerializerTest(TestCase):
    def test_valid_data(self):
        data={
            "positions":{
                "Queen": "A5", 
                "Bishop": "G8", 
                "Rook":"H5",
                "Knight":"G4"
            },
            "slug":"rook"
        }
        serializer=PositionSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
       
    #non-fields error
    def test_invalid_piece(self):
        data={
            "positions":{
                "Queen": "G2", 
                "Bishop": "H1", 
                "Rook":"H2",
                "Knight":"G1",
                "Pawn":"A2"
            },
            "slug":"rook"
        }
        serializer=PositionSerializer(data=data)
        self.assertFalse(serializer.is_valid(raise_exception=False))
        #serialize.errors is of type dictionary of size 1 with key=non_field_errors
        #It is a non_field_error because the validation is done by overriding the validate() i.e. it is a custom validation logic
        #the type of serialize.errors['non_field_errors'] is a list
        #serialize.errors['non_field_errors'][0] is an object of type ErrorDetail
        #However, its __str__ is overridden to written the string or the message it carries
       
        expected_error=[ErrorDetail(string="No such chess pieces. Invalid chess Pieces given in request data",code="invalid")]
        self.assertEqual(serializer.errors['non_field_errors'],expected_error)
        self.assertEqual(serializer.errors['non_field_errors'][0],expected_error[0])

    #fields error
    def test_missing_position(self):
        data={
            "positions": {
                "Queen": "", 
                "Bishop": "H1", 
                "Rook":"H2",
                "Knight":"G1",
            },
            "slug":"bishop"
        }
        serializer=PositionSerializer(data=data)
        self.assertFalse(serializer.is_valid(raise_exception=False))
        expected_error=[ErrorDetail(string='This field may not be blank.', code='blank')]
        #serialize.errors is of type dictionary with key='positions' 
        #serialize.errors[positions] is another dictionary whose keys are serializers.CharField()
        #by default CharFields() sets allow_blank to False
        #Hence positions=serializers.DictField(child=CharField()) fails validation since a key in positions dictionary i.e. Queen is blank
        #It is a field error. The field is 'positions'. The key in the dictionary is Queen at which the CharField is blank
        #That is the point where we get the ErrorDetail object which returns a string with error message
        self.assertEqual(serializer.errors['positions']['Queen'][0],expected_error[0])
        



class PositionViewTest(TestCase):
    def setUp(self):
        self.client=APIClient()
    
    def test_position_view_positive(self):
        request_data={"positions": {"Queen": "D5", "Bishop": "H1", "Rook":"A1","Knight":"F3"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,200)
        expected_response_data={"valid_moves": ["G2"]}
        self.assertEqual(response.content,JsonResponse(expected_response_data).content) 
    
    def test_position_view_missing_position(self):
        request_data={"positions": {"Queen": "", "Bishop": "H1", "Rook":"A1","Knight":"F3"}}
        response=self.client.post('/chess/knight/',request_data,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_position_view_invalid_position(self):
        request_data={"positions": {"Queen": "G2", "Bishop": "H1", "Rook":"N9","Knight":"G1"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,400)
    
    def test_position_view_duplicate_position(self):
        request_data={"positions": {"Queen": "G2", "Bishop": "G2", "Rook":"N9","Knight":"G1"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,400)

     

class ValidMovesTest(TestCase):

    def test_get_valid_moves(self):
        board={"Queen": "E7", "Bishop": "B7", "Rook":"G5","Knight":"C3"}
        slug="Knight"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["B1","D1","A4","A2"])
        self.assertSetEqual(output_set,expected_output_set)

