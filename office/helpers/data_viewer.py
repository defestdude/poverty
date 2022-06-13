from rest_framework import serializers

from landing.models import ProphetData

class PredictionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProphetData
        fields = (
            'id', 'ds', 'yhat','yhat_lower','yhat_upper'
        )