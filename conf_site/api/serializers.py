from rest_framework import serializers

from symposion.conference.models import Conference
from symposion.speakers.models import Speaker, User
from symposion.schedule.models import Presentation, Slot


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')

    class Meta:
        model = Speaker
        fields = ('username', 'name', 'email')


class ConferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conference
        exclude = ('id', 'timezone')


class SlotSerializer(serializers.ModelSerializer):
    day = serializers.StringRelatedField()
    kind = serializers.StringRelatedField()

    class Meta:
        model = Slot
        exclude = ('id', 'content_override', 'content_override_html')


class PresentationSerializer(serializers.ModelSerializer):
    speaker = SpeakerSerializer()
    slot = SlotSerializer()
    section = serializers.StringRelatedField()

    class Meta:
        model = Presentation
        exclude = ('id', 'description_html', 'abstract_html', 'proposal_base')
