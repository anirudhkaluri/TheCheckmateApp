from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import PositionSerializer
# Create your views here.

class PositionView(APIView):
    def post(self,request,slug,format='json'):
        #serialize the input json data
        serializer=PositionSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_details=e.detail
            return Response({'errors':error_details},status=400)
        deserialized_data=serializer.validated_data
        #board position in an ordered dictionary
        board=deserialized_data
        

        return Response({'message':deserialized_data})


