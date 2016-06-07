from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from symposion.conference.models import Conference
from symposion.speakers.models import Speaker

from .serializers import SpeakerSerializer, ConferenceSerializer


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


class ConferenceDetail(views.APIView):
    """
    Returns details about the Conference object in the
    Conference model.
    """

    def get(request, *args, **kwargs):
        conference = Conference.objects.first()
        serializer = ConferenceSerializer(conference)
        return Response(serializer.data)
