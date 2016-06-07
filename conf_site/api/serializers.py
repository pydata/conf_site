from rest_framework import serializers

from symposion.conference.models import Conference
from symposion.speakers.models import Speaker, User


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')

    class Meta:
        model = Speaker
        fields = ('username', 'name', 'email')


class ConferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conference
        exclude = ('id', 'timezone')
