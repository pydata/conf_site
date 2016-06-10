from rest_framework import viewsets
from rest_framework import response
from rest_framework.permissions import IsAdminUser
from symposion.speakers.models import Speaker

from .serializers import SpeakerSerializer


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Returns a the list of all speaker profiles.
    Allows lookups through the `id` parameter.
    """
    permission_classes = (IsAdminUser,)
    queryset = Speaker.objects.select_related(
        'user',
    ).filter(
        user__isnull=False,
    )
    serializer_class = SpeakerSerializer
