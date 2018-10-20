"""
We need new tests framework
"""
import os
from unittest import TestCase
from slack_entities.entities.team import Team


class TeamTestCase(TestCase):
    def test_get(self):
        team_name = os.environ.get('SLACK_TEAM_NAME')
        team = Team.get()

        self.assertEqual(team.name, team_name)
