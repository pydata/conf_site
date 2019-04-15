# -*- coding: utf-8 -*-
from django.test import TestCase

from symposion.schedule.tests.factories import (
    ConferenceFactory,
    SectionFactory,
)

from conf_site.proposals.tests.factories import ProposalFactory


class ProposalTestCase(TestCase):
    def setUp(self):
        # Create base conference infrastructure that has to exist in
        # order to create a Proposal.
        self.conference = ConferenceFactory()
        self.section = SectionFactory()
        self.proposal = ProposalFactory()
