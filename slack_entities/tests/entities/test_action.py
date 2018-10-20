"""
We need new tests framework
"""
from unittest import TestCase
from slack_entities.entities.action import action_from_webhook, Action, ButtonAction, SelectAction


WEBHOOK_TEMPLATE = {
    "type": "interactive_message",
    "callback_id": "callback",
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
    "original_message": {
        "text": "some text :)",
        "username": "BOT_USERNAME",
        "bot_id": "BOT_ID",
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
}
WEBHOOK_SELECT = dict(WEBHOOK_TEMPLATE, **{'actions': [{
    "name": "emails_list",
    "type": "select",
    "selected_options": [{
        "value": "5"
    }]
}]})
WEBHOOK_BUTTON = dict(WEBHOOK_TEMPLATE, **{'actions': [{
    "name": "ok",
    "type": "button",
    "value": "ok"
}]})
WEBHOOK_ACTION = dict(WEBHOOK_TEMPLATE, **{'actions': [{
    'type': 'something else'
}]})


class ActionTestCase(TestCase):
    def action_from_webhook_ButtonAction(self):
        action = action_from_webhook(WEBHOOK_BUTTON)

        self.assertTrue(type(action) == ButtonAction)

    def action_from_webhook_SelectAction(self):
        action = action_from_webhook(WEBHOOK_SELECT)

        self.assertTrue(type(action) == SelectAction)

    def action_from_webhook_Action(self):
        action = action_from_webhook(WEBHOOK_ACTION)

        self.assertTrue(type(action) == Action)

    def test_action_from_webhook(self):
        self.action_from_webhook_ButtonAction()
        self.action_from_webhook_SelectAction()
        self.action_from_webhook_Action()
