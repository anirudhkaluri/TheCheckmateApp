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

    #valid data sent to the serializer
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
        #since it is valid data the asserTrue must pass
        self.assertTrue(serializer.is_valid(raise_exception=True))
       
    
    #non-fields error raised by custom validation
    def test_invalid_piece(self):
        #Pawn is an invalid piece. 
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
        #serialize.errors['non_field_errors'][0] is an object of type ErrorDetail which consists of a string with error message
        #However, its __str__ is overridden to return the string or the message it carries
        expected_error=[ErrorDetail(string="No such chess pieces. Invalid chess Pieces given in request data",code="invalid")]
        self.assertEqual(serializer.errors['non_field_errors'],expected_error)
        self.assertEqual(serializer.errors['non_field_errors'][0],expected_error[0])


    #field error raised by Serializer
    def test_missing_position(self):
         #The position of the Queen is an empty string. 
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
        #positions is the field specified in the Serializer. its a field error at field='positions'
        #The key in the dictionary  is Queen at which the CharField is blank. by default CharFields() sets allow_blank to False
        #Hence positions=serializers.DictField(child=CharField()) fails validation since a key in positions dictionary i.e. Queen is blank
        #serialize.errors[positions] is another dictionary whose key is 'queen' which is serializers.CharField() but got an empty string
        #That is the point where we get the ErrorDetail object which returns a string with error message
        self.assertEqual(serializer.errors['positions']['Queen'][0],expected_error[0])
        






#To test the PositionView in chess/views.py
class PositionViewTest(TestCase):
    def setUp(self):
        self.client=APIClient()
    
    #testing for a positive outcome 
    def test_position_view_positive(self):
        request_data={"positions": {"Queen": "D5", "Bishop": "H1", "Rook":"A1","Knight":"F3"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,200)
        expected_response_data={"valid_moves": ["G2"]}
        #both expected outcome and actual response must be same
        self.assertEqual(response.content,JsonResponse(expected_response_data).content) 
        
    
    #testing for invalid position for Rook at N9. N9 is invalid position. 
    def test_position_view_invalid_position(self):
        request_data={"positions": {"Queen": "G2", "Bishop": "H1", "Rook":"N9","Knight":"G1"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,400)
    
    #testing for two pieces at the same position. The serialization validation fails. The view will return a 400 code
    #Both queen and bishop occupy G2 
    def test_position_view_duplicate_position(self):
        request_data={"positions": {"Queen": "G2", "Bishop": "G2", "Rook":"A8","Knight":"G1"}}
        response=self.client.post('/chess/bishop/',request_data,format='json')
        self.assertEqual(response.status_code,400)

     







#Testing the get_valid_moves method in chess/utils/validMoves.py module
#get_valid_moves is called only after thorough validation by serializer
#hence the test cases here must be only valid test cases without invalid pieces, invalid positions, invalid slugs
class ValidMovesTest(TestCase):

    def test_get_valid_moves1(self):
        board={"Queen": "E7", "Bishop": "B7", "Rook":"G5","Knight":"C3"}
        slug="Knight"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["B1","D1","A4","A2"])
        self.assertSetEqual(output_set,expected_output_set)
    

    def test_get_valid_moves2(self):
        board={"Queen": "H1", "Bishop": "A8", "Rook":"H8","Knight":"D3"}
        slug="Queen"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["H8", "G1", "F1", "D1", "B1", "A1"])
        self.assertSetEqual(output_set,expected_output_set)

    

    def test_get_valid_moves3(self):
        board={"Queen": "G2", "Bishop": "H1", "Rook":"H2","Knight":"G1"}
        slug="Bishop"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        #expected valid moves will be 0 for Bishop in this configuration
        expected_output_set=set([])
        self.assertSetEqual(output_set,expected_output_set)


    def test_get_valid_moves4(self):
        board={"Queen": "A1", "Bishop": "G5", "Rook":"D5","Knight":"H8"}
        slug="Rook"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["D3", "D6", "D7", "F5", "G5", "C5", "B5"])
        self.assertSetEqual(output_set,expected_output_set)


    def test_get_valid_moves5(self):
        board={"Queen": "D5", "Bishop": "H1", "Rook":"A1","Knight":"F3"}
        slug="Bishop"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        expected_output_set=set(["G2"])
        self.assertSetEqual(output_set,expected_output_set)

    
    def test_get_valid_moves6(self):
        board={"Queen": "F3", "Bishop": "H1", "Rook":"H8","Knight":"G5"}
        slug="Bishop"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        #expected output will be empty for this configuration
        expected_output_set=set([])
        self.assertSetEqual(output_set,expected_output_set)
    
    def test_get_valid_moves7(self):
        board={"Queen": "D7", "Bishop": "E6", "Rook":"D5","Knight":"C6"}
        slug="Rook"
        output=get_valid_moves(board,slug)
        output_set=set(output)
        #expected output will be empty for this configuration
        expected_output_set=set(["G5", "H5", "C5", "B5"])
        self.assertSetEqual(output_set,expected_output_set)
