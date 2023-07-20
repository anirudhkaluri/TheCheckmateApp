from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
from .utils.validMoves import get_valid_moves
from django.http import JsonResponse
import logging
import json
from django.core.cache import cache
import re

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
            #log both request data and error whenever there is an error
            logger.error(f"{error_details} for the data {request.data}")
            return Response({'errors':error_details},status=400)

        #Get data from the serializer.
        # board is the configuration of the chess board in the form of dictioanry "piece":"piece_position" 
        board=serializer.validated_data['positions']
        #slug is the piece for which we find the valid moves
        slug=serializer.validated_data['slug']

        #search in the cache and if present return the result
        [cached_response,cache_key]=get_from_cache(board,slug)
        if cached_response is not None:
            return JsonResponse(cached_response) #return response if there is a chached key

        # use get_valid_moves to get all moves which the slug can take given the board's configuration
        valid_moves= get_valid_moves(board,slug)

        #send response
        response_data={
            'valid_moves':valid_moves
        }
        #set cache key and enter the request into the cache
        #The default time is set to none i.e. it  will persis in cache until it is not cleared,explicitly deleted, or full capcity
        cache.set(cache_key,response_data,60*2)

        return JsonResponse(response_data)

#handles caching operations
def get_from_cache(board:dict[str,str],slug:str)->list:
    new_dict=dict(board)
    new_dict['slug']=slug
    #since input is a dictionary serialize it to json to create a cache key
    #sort the keys. the keys are limited and are unique.
    cache_key=json.dumps(new_dict,sort_keys=True)
    #remove special character from cache key. Not recommended to generate cache key with special characters.
    cache_key = re.sub(r'[,":{} ]', '', cache_key) #regular expression to remove special characters
    cached_response=cache.get(cache_key)
    return [cached_response,cache_key]


#FUTURE DEVELOPEMENT: implement cache eviction policies when cache is full