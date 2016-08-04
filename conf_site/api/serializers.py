from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from symposion.conference.models import Conference
from symposion.speakers.models import Speaker, User
from symposion.schedule.models import Presentation, Slot
from symposion.sponsorship.models import Sponsor, SponsorLevel


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse_lazy(
            'speaker_profile',
            kwargs={'pk': obj.pk},
            request=self.context['request'],
        )

    class Meta:
        model = Speaker
        fields = (
            'username',
            'name',
            'email',
            'absolute_url',
        )


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
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse_lazy(
            'schedule_presentation_detail',
            args=[obj.pk],
            request=self.context['request'],
        )

    class Meta:
        model = Presentation
        exclude = ('id', 'description_html', 'abstract_html', 'proposal_base')


class SponsorLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SponsorLevel
        fields = ('name', 'cost')


class SponsorSerializer(serializers.ModelSerializer):
    level = SponsorLevelSerializer()
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse_lazy(
            'sponsor_detail',
            kwargs={'pk': obj.pk},
            request=self.context['request'],
        )

    class Meta:
        model = Sponsor
        fields = (
            'name',
            'external_url',
            'contact_name',
            'contact_email',
            'level',
            'absolute_url',
            'annotation',
        )
