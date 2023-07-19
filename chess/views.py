from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
from .utils import validMoves
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
        valid_moves= validMoves(board,slug.title())
        return Response({'message':valid_moves})


