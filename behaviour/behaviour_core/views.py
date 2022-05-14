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

class MouseApiView(APIView):
    queryset = Mouse.objects.all().order_by('id')
    serializer_class = MouseSerializer

    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        mouse_data = Mouse.objects.all().order_by('id')#Mouse.objects.filter(user = request.user.id)
        mouse_serializer = MouseSerializer(mouse_data, many=True)
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
