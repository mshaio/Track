from urllib import response
from django.shortcuts import render

# Create your views here.
# from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import MouseSerializer
from .models import Mouse

from behaviour.lib.track import Track
from behaviour.lib.analyse import Analyse

class MouseApiView(APIView):
    queryset = Mouse.objects.all().order_by('id')
    serializer_class = MouseSerializer

    def get(self, request, *args, **kwargs):
        '''
        Get all mouse movement data, if certain parameters are present, response varies
        ie, you can pass in 'computed' parameter:
        http://127.0.0.1:8000/behaviour_core/mouse?computed=true
        '''
        mouse_data = Mouse.objects.all().order_by('id')#Mouse.objects.filter(user = request.user.id)
        mouse_serializer = MouseSerializer(mouse_data, many=True)
        analyse = Analyse(None, mouse_serializer.data)

        response_computed = {}
        response_computed['gradient_count_by_type'] = analyse.get_gradient_count_by_type()
        response_computed['magnitude_by_frequency'] = analyse.get_magnitude_by_frequency()
        response_computed['direction_by_frequency'] = analyse.get_direction_by_frequency()
        response_computed['mouse_movement_duration_frequency'] = analyse.get_mouse_movement_duration_by_frequency()

        if request.query_params.get('computed'):
            return Response(response_computed, status=status.HTTP_200_OK)

        return Response(mouse_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'x_coord': request.data.get('x_coord'), 
            'y_coord': request.data.get('y_coord'),
            'category': request.data.get('category'), 
        }
        # Track.test()
        print(f'data: {data}')
        serializer = MouseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class MouseViewSet(viewsets.ModelViewSet):
#     queryset = Mouse.objects.all().order_by('id')
#     serializer_class = MouseSerializer
