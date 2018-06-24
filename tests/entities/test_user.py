from django.test import SimpleTestCase

from slack.entities.user import User


class UserTestCase(SimpleTestCase):
    def test_get_filter(self):
        # Getting user by id
        user_1 = User.get(id="U2GUL0QF9")

        # Getting user from list
        user_2 = User.filter(id=user_1.id)[0]

        # Should be equal
        self.assertEqual(user_1, user_2)
