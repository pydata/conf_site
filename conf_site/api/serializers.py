from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from symposion.conference.models import Conference
from symposion.speakers.models import Speaker
from symposion.schedule.models import Presentation, Slot


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse_lazy(
            'speaker_profile',
            kwargs={"pk": obj.pk, "slug": obj.slug},
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
        exclude = ('id',)


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
            args=[obj.pk, obj.slug],
            request=self.context['request'],
        )

    class Meta:
        model = Presentation
        exclude = ('id', 'description_html', 'abstract_html', 'proposal_base')
