import logging

from slack_entities.entities.channel import Channel
from slack_entities.entities.team import Team
from slack_entities.entities.user import User
from .incoming_message import IncomingMessage


logger = logging.getLogger('action_factory')


class Action:
    """
    Represents Slack's action
    """
    def __init__(
            self,
            ts,
            callback_id,
            team: Team,
            channel: Channel,
            user: User,
            original_message: IncomingMessage
    ):
        self.ts = ts
        self.callback_id = callback_id
        self.team = team
        self.channel = channel
        self.user = user
        self.original_message = original_message

    @classmethod
    def _get_original_message(cls, webhook):
        original_message = webhook['original_message']

        return IncomingMessage(
            user_id=original_message.get('user') or original_message.get('bot_id'),
            channel_id=webhook['channel']['id'],
            text=original_message['text'],
            attachments=original_message.get('attachments', list())
        )

    @classmethod
    def from_item(cls, webhook):
        team_dict = webhook['team']
        channel_dict = webhook['channel']
        user_dict = webhook['user']

        ts = webhook['action_ts']
        callback_id = webhook['callback_id']
        team = Team(id=team_dict['id'], domain=team_dict['domain'])
        channel = Channel(id=channel_dict['id'], name=channel_dict['name'])
        user = User(id=user_dict['id'], name=user_dict['name'])
        original_message = cls._get_original_message(webhook)

        return cls(ts, callback_id, team, channel, user, original_message)

    def __repr__(self):
        return f'<{self.__class__.__name__} {{ts: {self.ts}}}>'


class SelectAction(Action):
    """
    Represents Slack's select action type
    """
    def __init__(
            self,
            ts,
            callback_id,
            name,
            value,
            team: Team,
            channel: Channel,
            user: User,
            original_message: IncomingMessage
    ):
        super().__init__(ts, callback_id, team, channel, user, original_message)
        self.name = name
        self.value = value

    @classmethod
    def from_item(cls, webhook):
        action = webhook['actions'][0]
        team_dict = webhook['team']
        channel_dict = webhook['channel']
        user_dict = webhook['user']

        ts = webhook['action_ts']
        callback_id = webhook['callback_id']
        name = action['name']
        value = action['selected_options'][0]['value']
        team = Team(id=team_dict['id'], domain=team_dict['domain'])
        channel = Channel(id=channel_dict['id'], name=channel_dict['name'])
        user = User(id=user_dict['id'], name=user_dict['name'])
        original_message = cls._get_original_message(webhook)

        return cls(ts, callback_id, name, value, team, channel, user, original_message)


class ButtonAction(Action):
    """
    Represents Slack's button action type
    """
    def __init__(
            self,
            ts,
            callback_id,
            name,
            value,
            team: Team,
            channel: Channel,
            user: User,
            original_message: IncomingMessage
    ):
        super().__init__(ts, callback_id, team, channel, user, original_message)
        self.name = name
        self.value = value

    @classmethod
    def from_item(cls, webhook):
        action = webhook['actions'][0]
        team_dict = webhook['team']
        channel_dict = webhook['channel']
        user_dict = webhook['user']

        ts = webhook['action_ts']
        callback_id = webhook['callback_id']
        name = action['name']
        value = action['value']
        team = Team(id=team_dict['id'], domain=team_dict['domain'])
        channel = Channel(id=channel_dict['id'], name=channel_dict['name'])
        user = User(id=user_dict['id'], name=user_dict['name'])
        original_message = cls._get_original_message(webhook)

        return cls(ts, callback_id, name, value, team, channel, user, original_message)


def get_action_class(action_type):
    """
    Returns class that should be used for the action
    """
    if action_type == 'select':
        return SelectAction

    if action_type == 'button':
        return ButtonAction

    return Action


def get_action_from_webhook(webhook):
    action = webhook['actions'][0]
    return get_action_class(action.get('type')).from_item(webhook)


def action_from_webhook(webhook):
    """
    Returns Action object from the webhook
    """
    logger.info(f"Parsing action from webhook with timestamp: {webhook['action_ts']}")
    action = get_action_from_webhook(webhook)
    logger.info(f'Parsed {action}')
    return action
