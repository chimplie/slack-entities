"""
We need new tests framework
"""
import os
from unittest import TestCase
from slack_entities.entities.team import Team


class TeamTestCase(TestCase):
    def test_get(self):
        team_id = os.environ.get('SLACK_TEAM_ID', 'TBLEMQT2M')
        team_name = os.environ.get('SLACT_TEAM_NAME', 'UTS Chatbot')

        # Getting team by id
        team = Team.get(id=team_id)

        self.assertEqual(team.name, team_name)
