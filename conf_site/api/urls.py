from django.conf.urls import include, re_path
from rest_framework.routers import SimpleRouter

from . import views


# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register(r'speaker', views.SpeakerViewSet)
router.register(r'presentation', views.PresentationViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^$', views.ConferenceDetail.as_view(), name='conference-detail'),
]
