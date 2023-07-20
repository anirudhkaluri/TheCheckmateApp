from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
from .utils.validMoves import get_valid_moves
from django.http import JsonResponse
import logging


logger=logging.getLogger('chess.views')



class PositionView(APIView):
    def post(self,request,slug,format='json'):
        
        #deserialize the input json data
        request.data['slug']=slug
        serializer=PositionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_details=e.detail
            logger.info(f"Error for the data {request.data}")
            logger.error(error_details)
            return Response({'errors':error_details},status=400)

        #board is a dictionary with position as the only key 
        board=serializer.validated_data['positions']
        slug=serializer.validated_data['slug']
       

        # board[positions] is an ordered dictionary with locations of teh pieces
        valid_moves= get_valid_moves(board,slug)
        response_data={
            'valid_moves':valid_moves
        }
        return JsonResponse(response_data)


