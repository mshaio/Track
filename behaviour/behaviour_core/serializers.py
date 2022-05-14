from rest_framework import serializers

from .models import Mouse

class MouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mouse
        fields = ('id','x_coord', 'y_coord', 'category')