from rest_framework import serializers
from .models import Paste, PasteAnalytic


class PasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paste
        fields = ['key', 'content']


class PasteAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasteAnalytic
        fields = ['view_count', 'created_at']
