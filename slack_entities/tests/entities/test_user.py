"""
We need new tests framework
"""
import os
from unittest import TestCase
from slack_entities.entities.user import User


class UserTestCase(TestCase):
    def test_get_filter(self):
        user_id = os.environ.get('SLACK_USER_ID')

        # Getting user by id
        user_1 = User.get(id=user_id)

        # Getting user from list
        user_2 = User.filter(id=user_1.id)[0]

        # Should be equal
        self.assertEqual(user_1, user_2)
