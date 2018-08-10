"""
We need new tests framework
"""
from unittest import TestCase
from slack_entities.entities.channel import Channel


class ChannelTestCase(TestCase):
    def test_get(self):
        # Getting channel by name
        channel_1 = Channel.get(name="general")

        # Getting channel by id
        channel_2 = Channel.get(id=channel_1.id)

        self.assertEqual(channel_1, channel_2)
