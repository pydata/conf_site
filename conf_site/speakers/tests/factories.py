# -*- coding: utf-8 -*-
import factory

from symposion.speakers.models import Speaker

from conf_site.accounts.tests.factories import UserFactory


class SpeakerFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    speaker_timezone = factory.Faker("timezone")

    class Meta:
        model = Speaker
