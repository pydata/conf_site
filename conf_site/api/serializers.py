from rest_framework import serializers

from symposion.speakers.models import Speaker, User


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')

    class Meta:
        model = Speaker
        fields = ('username', 'name', 'email')
