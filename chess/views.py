from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
from .utils.validMoves import get_valid_moves
# Create your views here.

class PositionView(APIView):
    def post(self,request,slug,format='json'):
        
        #deserialize the input json data
        serializer=PositionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_details=e.detail
            return Response({'errors':error_details},status=400)

        #board position in an ordered dictionary
        board=serializer.validated_data
        valid_moves= get_valid_moves(board,slug)
        return Response({'message':valid_moves})


