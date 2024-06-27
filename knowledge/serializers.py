from rest_framework import serializers


class KnowledgeCreateSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    openai_api_key = serializers.CharField(required=True)


class KnowledgeDeleteSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    openai_api_key = serializers.CharField(required=True)


class KnowledgeRetrieveSerializer(serializers.Serializer):
    openai_api_key = serializers.CharField(required=True)
    question = serializers.CharField(required=True)
