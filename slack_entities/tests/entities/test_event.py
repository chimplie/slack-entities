"""
We need new tests framework
"""
from unittest import TestCase

from slack_entities.entities.event import event_from_webhook, MessageEvent, EditedMessageEvent


class EditedMessageEventTestCase(TestCase):
    def test_event_from_webhook(self):
        self.event_from_webhook_MessageEvent()
        self.event_from_webhook_EditedMessageEvent()

    def event_from_webhook_MessageEvent(self):
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

    def event_from_webhook_EditedMessageEvent(self):
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
