from rest_framework import serializers
from models import ChannelModel

class ChannelModelSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=500)
    url = serializers.CharField()
    def create(self, validated_data):
        return ChannelModel.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance