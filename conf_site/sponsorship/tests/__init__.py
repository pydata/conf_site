import factory

from symposion.schedule.tests.factories import ConferenceFactory
from symposion.sponsorship.models import SponsorLevel, Sponsor


class SponsorLevelFactory(factory.django.DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    name = factory.Faker("color_name")
    order = factory.Faker("pyint")
    cost = factory.Faker("pyint")
    description = factory.Faker("paragraph")

    class Meta:
        model = SponsorLevel


class SponsorFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    display_url = factory.Faker("uri")
    external_url = factory.Faker("uri")
    contact_name = factory.Faker("name")
    contact_email = factory.Faker("company_email")
    level = factory.SubFactory(SponsorLevelFactory)
    active = factory.Faker("boolean")

    class Meta:
        model = Sponsor
