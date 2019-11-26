"""
We need new tests framework
"""
from unittest import TestCase

from slack_entities.entities.event import event_from_webhook, MessageEvent, EditedMessageEvent, UserChangeEvent, \
    TeamJoinEvent, DeletedMessageEvent, event_from_rtm, BotMessageEvent


class MessageEventTestCase(TestCase):
    def test_from_item(self):
        text = 'text in MessageEvent'
        webhook = {
            'event_id': 'Q1W2E3R4T5',
            'event': {
                'type': 'message',
                'user': 'user_id',
                'channel': 'channel_id',
                'text': text,
            }
        }
        event = event_from_webhook(webhook)

        self.assertTrue(type(event) is MessageEvent)
        self.assertEqual(text, event.message.text)

    def test_from_rtm(self):
        text = 'text in RTM event'
        event_id = 'event_id'
        rtm_event = {
            'client_msg_id': '9455e012-8993-4de0-95e1-dc0ef00d9dc0',
            'suppress_notification': False,
            'text': text,
            'user': 'user_id',
            'team': 'teamid',
            'user_team': 'teamid',
            'source_team': 'teamid',
            'channel': 'channelid',
            'event_ts': event_id,
            'ts': '1570352396.004200'}

        event = event_from_rtm(rtm_event, 'message')

        self.assertTrue(type(event) is MessageEvent)
        self.assertEqual(text, event.message.text)
        self.assertEqual(event_id, event.id)


class EditedMessageEventTestCase(TestCase):
    def test_from_item(self):
        text = 'text in EditedMessage'
        attachments = [
            {
                'lol': 'wut'
            },
            {
                'wut': 'lol'
            }
        ]
        prev_text = 'text in previous message'
        prev_attachments = [
            {
                'lol': 'wut'
            }
        ]
        bot_id = 'BC29QGAGY'
        webhook = {
            'event_id': 'Q1W2E3R4T5',
            'event': {
                'type': 'message',
                'message': {
                    'text': text,
                    'bot_id': bot_id,
                    'type': 'message',
                    'subtype': 'bot_message',
                    'attachments': attachments
                },
                'channel': 'channel_id',
                'subtype': 'message_changed',
                'previous_message': {
                    'text': prev_text,
                    'username': 'dev DC-D2',
                    'bot_id': 'BC29QGAGY',
                    'attachments': prev_attachments
                }
            }
        }
        event = event_from_webhook(webhook)

        self.assertTrue(type(event) is EditedMessageEvent)
        self.assertEqual(text, event.message.text)
        self.assertEqual(attachments, event.message.attachments)
        self.assertEqual(prev_text, event.previous_message.text)
        self.assertEqual(prev_attachments, event.previous_message.attachments)


class DeletedMessageEventTestCase(TestCase):
    def test_from_item(self):
        deleted_text = 'text in DeletedMessage'
        deleted_attachments = [
            {
                'lol': 'wut'
            },
            {
                'wut': 'lol'
            }
        ]
        webhook = {
            'event_id': 'Q1W2E3R4T5',
            'type': 'event_callback',
            'event': {
                'type': 'message',
                'channel': 'channel_id',
                'subtype': 'message_deleted',
                'previous_message': {
                    'type': 'message',
                    'text': deleted_text,
                    'files': [],
                    'user': 'user_id',
                    'attachments': deleted_attachments
                }
            }
        }
        event = event_from_webhook(webhook)

        self.assertTrue(type(event) is DeletedMessageEvent)
        self.assertEqual(deleted_text, event.message.text)
        self.assertEqual(deleted_attachments, event.message.attachments)


class UserChangeEventTestCase(TestCase):
    def test_from_item(self):
        user_id = 'U1234'
        user_name = 'Test User'

        webhook = {
            'event_id': 'blabla',
            'event': {
                'type': 'user_change',
                'user': {
                    'id': user_id,
                    'name': user_name,
                    'profile': {
                        'title': 'lol',
                        'phone': '228',
                        'real_name': 'Lol'
                    }
                }
            }
        }

        event = event_from_webhook(webhook)

        self.assertEqual(type(event), UserChangeEvent)
        self.assertEqual(event.user.id, user_id)
        self.assertEqual(event.user.name, user_name)


class TeamJoinEventTestCase(TestCase):
    def test_from_item(self):
        user_id = 'U1234'
        user_name = 'Test User'

        webhook = {
            'event_id': 'blabla',
            'event': {
                'type': 'team_join',
                'user': {
                    'id': user_id,
                    'name': user_name,
                    'profile': {
                        'title': 'lol',
                        'phone': '228',
                        'real_name': 'Lol'
                    }
                }
            }
        }

        event = event_from_webhook(webhook)

        self.assertEqual(type(event), TeamJoinEvent)
        self.assertEqual(event.user.id, user_id)
        self.assertEqual(event.user.name, user_name)


class BotMessageEventTestCase(TestCase):
    def test_from_item(self):
        text = 'text in MessageEvent'
        webhook = {
            'event_id': 'Q1W2E3R4T5',
            'event': {
                'type': 'message',
                'subtype': 'bot_message',
                'bot_id': 'someid',
                'channel': 'channel_id',
                'text': text,
            }
        }
        event = event_from_webhook(webhook)

        self.assertTrue(type(event) is BotMessageEvent)
        self.assertEqual(text, event.message.text)
