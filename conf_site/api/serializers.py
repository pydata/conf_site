from django.core.urlresolvers import reverse_lazy

from rest_framework import serializers

from symposion.conference.models import Conference
from symposion.speakers.models import Speaker, User
from symposion.sponsorship.models import Sponsor


class SpeakerSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user')
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return reverse_lazy('speaker_profile', kwargs={'pk': obj.pk})

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


class SponsorSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(read_only=True, slug_field='name')
    absolute_url = serializers.URLField(source='get_absolute_url')

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
