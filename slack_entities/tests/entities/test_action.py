"""
We need new tests framework
"""
from unittest import TestCase
from slack.web.classes.blocks import SectionBlock, DividerBlock, ActionsBlock
from slack.web.classes.elements import ButtonElement

from slack_entities.entities.action import (
    action_from_webhook, Action, ButtonAction, SelectAction,
    MessageAction, DialogSubmissionAction, BlockAction
)


def return_original_message():
    return {
        "text": "some text :)",
        "username": "BOT_USERNAME",
        "bot_id": "BOT_ID",
        "team": "TEAM_ID",
        "attachments": [{
            "callback_id": "first_callback",
            "fallback": "Try again later :(",
            "text": "text for action:",
            "id": 1,
            "color": "3AA3E3",
            "actions": [{
                "id": "1",
                "name": "ACTION_NAME",
                "text": "placeholder",
                "type": "select",
                "data_source": "static",
                "options": [{
                    "text": "1",
                    "value": "1"
                }]
            }]
        }],
        "type": "message",
        "subtype": "bot_message"
    }


WEBHOOK_TEMPLATE = {
    "type": "interactive_message",
    "callback_id": "test_callback_id",
    "team": {
        "id": "TEAM_ID",
        "domain": "TEAM_DOMAIN"
    },
    "channel": {
        "id": "CHANNEL_ID",
        "name": "CHANNEL_NAME"
    },
    "user": {
        "id": "USER_ID",
        "name": "USER_NAME"
    },
    "action_ts": "1539762867.466414",
    "token": "SLACK_TOKEN",
    "response_url": 'test_url',
}
WEBHOOK_SELECT = dict(WEBHOOK_TEMPLATE, **{
    'actions': [{
        "name": "emails_list",
        "type": "select",
        "selected_options": [{
            "value": "5"
        }]
    }],
    "original_message": return_original_message(),
    'response_url': 'test_url',
    'trigger_id': 'test_trigger_id'
})
WEBHOOK_BUTTON = dict(WEBHOOK_TEMPLATE, **{
    'actions': [{
        "name": "ok",
        "type": "button",
        "value": "ok"
    }],
    "original_message": return_original_message(),
    'response_url': 'test_url',
    'trigger_id': 'test_trigger_id'
})
WEBHOOK_ACTION = dict(WEBHOOK_TEMPLATE, **{
    'actions': [{
        'type': 'something else'
    }],
    'original_message': return_original_message(),
    'response_url': 'test_url'
})
WEBHOOK_MESSAGE_ACTION = dict(WEBHOOK_TEMPLATE, **{
    'type': 'message_action',
    'callback_id': 'pivotal',
    'trigger_id': '472869436786.47444502659.884405da2a25311a4bcae9ddfaf23c07',
    'message': {
        'text': "some message",
        'username': 'USERNAME',
        'user': 'USER_ID',
        'type': 'message',
        'ts': '1541507772.003300'
    },
    'response_url': 'test_url'
})
WEBHOOK_DIALOG_SUBMISSION_ACTION = dict(WEBHOOK_TEMPLATE, **{
    'type': 'dialog_submission',
    'callback_id': 'pivotal-ticket',
    'submission': {
        'field_1': 'val 1',
        'field_2': 'val 2'
    },
    'response_url': 'test_url'
})

# TODO Add 'block_id' and 'action_id' where needed
WEBHOOK_BLOCK_ACTION = dict(WEBHOOK_TEMPLATE, **{
    'type': 'block_actions',
    "actions": [
        {
            'action_id': 'WaXA',
            'block_id': '=qXel',
            'value': 'click_me_123',
            'action_ts': '1548426417.840180'
        }
    ],
    'trigger_id': 'some trigger id',
    'message': {
        'text': 'some message',
        'user': 'USER_ID',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'text': 'Text in section.'
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'text': 'Button',
                    },
                    'value': 'click_me_123'
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'text': 'Button',
                        },
                        'value': 'click_me_123'
                    }
                ]
            }
        ]
    },
})


class ActionTestCase(TestCase):
    def action_from_webhook_ButtonAction(self):
        action = action_from_webhook(WEBHOOK_BUTTON)

        self.assertTrue(action.trigger_id == 'test_trigger_id')
        self.assertTrue(action.response_url == 'test_url')
        self.assertTrue(type(action) == ButtonAction)

    def action_from_webhook_SelectAction(self):
        action = action_from_webhook(WEBHOOK_SELECT)

        self.assertTrue(action.trigger_id == 'test_trigger_id')
        self.assertTrue(action.response_url == 'test_url')
        self.assertTrue(type(action) == SelectAction)

    def action_from_webhook_Action(self):
        action = action_from_webhook(WEBHOOK_ACTION)

        self.assertTrue(action.callback_id == 'test_callback_id')
        self.assertTrue(type(action) == Action)

    def action_from_webhook_MessageAction(self):
        action = action_from_webhook(WEBHOOK_MESSAGE_ACTION)

        self.assertTrue(action.callback_id == 'pivotal')
        self.assertTrue(action.trigger_id == '472869436786.47444502659.884405da2a25311a4bcae9ddfaf23c07')
        self.assertTrue(action.response_url == 'test_url')
        self.assertTrue(type(action) == MessageAction)

    def action_from_webhook_DialogSubmissionAction(self):
        action = action_from_webhook(WEBHOOK_DIALOG_SUBMISSION_ACTION)

        self.assertTrue(action.callback_id == 'pivotal-ticket')
        self.assertTrue(action.response_url == 'test_url')
        self.assertTrue(action.submission == {
            'field_1': 'val 1',
            'field_2': 'val 2'
        })
        self.assertTrue(type(action) == DialogSubmissionAction)

    def action_from_webhook_BlockAction(self):
        action = action_from_webhook(WEBHOOK_BLOCK_ACTION)

        self.assertTrue(type(action.original_message.blocks[0]) == SectionBlock)
        self.assertTrue(type(action.original_message.blocks[1]) == DividerBlock)
        self.assertTrue(type(action.original_message.blocks[2]) == ActionsBlock)
        self.assertTrue(type(action.original_message.blocks[0].accessory) == ButtonElement)
        self.assertTrue(type(action.original_message.blocks[2].elements[0]) == ButtonElement)
        self.assertTrue(type(action) == BlockAction)

    def test_action_from_webhook(self):
        self.action_from_webhook_ButtonAction()
        self.action_from_webhook_SelectAction()
        self.action_from_webhook_Action()
        self.action_from_webhook_MessageAction()
        self.action_from_webhook_DialogSubmissionAction()
        self.action_from_webhook_BlockAction()
