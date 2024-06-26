from rest_framework import serializers


class KnowledgeSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    openai_api_key = serializers.CharField(required=True)
