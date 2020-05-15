# serializers.py
from rest_framework import serializers

from .models import Tags, Activities, FinalResult, Paragraphs


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class ActivitiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activities
        fields = '__all__'

class FinalResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinalResult
        fields = '__all__'

class ParagraphsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paragraphs
        fields = '__all__'