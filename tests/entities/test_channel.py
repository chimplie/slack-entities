from django.test import SimpleTestCase

from slack.entities.channel import Channel


class ChannelTestCase(SimpleTestCase):
    def test_get(self):
        # Getting channel by name
        channel_1 = Channel.get(name="daily_update")

        # Getting channel by id
        channel_2 = Channel.get(id=channel_1.id)

        self.assertEqual(channel_1, channel_2)
