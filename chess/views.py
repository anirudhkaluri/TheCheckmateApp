from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
from .utils.validMoves import get_valid_moves
from django.http import JsonResponse
import logging

#define a logger 
#all logs in project.log in root directory
logger=logging.getLogger('chess.views')



class PositionView(APIView):
    def post(self,request,slug,format='json'):
        
        request.data['slug']=slug

        #Send data to serializer to deserialize and validate
        serializer=PositionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_details=e.detail
            #log both request data and error whenever there is an error/exception
            logger.info(f"Error for the data {request.data}")
            logger.error(error_details)
            return Response({'errors':error_details},status=400)

        #Get data from the serializer.
        # board is the configuration of the chess board in the form of dictioanry "piece":"piece_position" 
        board=serializer.validated_data['positions']
        #slug is the piece for which we find the valid moves
        slug=serializer.validated_data['slug']
       

        # use get_valid_moves to get all moves which the slug can take given the board's configuration
        valid_moves= get_valid_moves(board,slug)

        #send response
        response_data={
            'valid_moves':valid_moves
        }
        return JsonResponse(response_data)


