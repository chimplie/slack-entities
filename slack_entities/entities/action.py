import logging

from slack_entities.entities.channel import Channel
from slack_entities.entities.team import Team
from slack_entities.entities.user import User
from .incoming_message import IncomingMessage


logger = logging.getLogger('action_factory')


# class BaseAction:
#     """
#     Base class for slack's action
#     """
#     def __init__(
#             self,
#             ts,
#             callback_id,
#             team: Team,
#             channel: Channel,
#             user: User,
#     ):
#         self.ts = ts
#         self.callback_id = callback_id
#         self.team = team
#         self.channel = channel
#         self.user = user
#
#     @classmethod
#     def from_item(cls, webhook):
#         raise NotImplementedError('It\'s an abstract class for slack\'s action')


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


class MessageAction(Action):
    """
    Represents custom slack user action
    """
    def __init__(
            self,
            ts,
            callback_id,
            trigger_id,
            response_url,
            team: Team,
            channel: Channel,
            user: User,
            original_message: IncomingMessage
    ):
        super().__init__(ts, callback_id, team, channel, user, original_message)
        self.trigger_id = trigger_id
        self.response_url = response_url

    @classmethod
    def from_item(cls, webhook):
        team_dict = webhook['team']
        channel_dict = webhook['channel']
        user_dict = webhook['user']

        ts = webhook['action_ts']
        callback_id = webhook['callback_id']
        trigger_id = webhook['trigger_id']
        response_url = webhook['response_url']
        team = Team(id=team_dict['id'], domain=team_dict['domain'])
        channel = Channel(id=channel_dict['id'], name=channel_dict['name'])
        user = User(id=user_dict['id'], name=user_dict['name'])

        original_message = cls._get_message(webhook)

        return cls(ts, callback_id, trigger_id, response_url, team, channel, user, original_message)

    @classmethod
    def _get_original_message(cls, webhook):
        raise NotImplementedError('You can\'t use this method in MessageAction class')

    @classmethod
    def _get_message(cls, webhook):
        message = webhook['message']

        return IncomingMessage(
            user_id=message.get('user') or message.get('bot_id'),
            channel_id=webhook['channel']['id'],
            text=message['text'],
            attachments=message.get('attachments', list())
        )


class DialogSubmissionAction(Action):
    """
    Represents dialog submission action
    """
    def __init__(
            self,
            ts,
            callback_id,
            response_url,
            submission: dict,
            team: Team,
            channel: Channel,
            user: User
    ):
        super().__init__(ts, callback_id, team, channel, user, None)
        self.response_url = response_url
        self.submission = submission

    @classmethod
    def from_item(cls, webhook):
        team_dict = webhook['team']
        channel_dict = webhook['channel']
        user_dict = webhook['user']

        ts = webhook['action_ts']
        callback_id = webhook['callback_id']
        response_url = webhook['response_url']
        submission = webhook['submission']
        team = Team(id=team_dict['id'], domain=team_dict['domain'])
        channel = Channel(id=channel_dict['id'], name=channel_dict['name'])
        user = User(id=user_dict['id'], name=user_dict['name'])

        return cls(ts, callback_id, response_url, submission, team, channel, user)


def get_class_for_interactive_message(action_type):
    """
    Returns one of classes which handle actions with type 'interactive_message'
    """
    if action_type == 'select':
        return SelectAction

    if action_type == 'button':
        return ButtonAction

    return Action


def get_action_from_webhook(webhook):
    _type = webhook['type']

    if _type == 'interactive_message':
        return get_class_for_interactive_message(webhook['actions'][0].get('type')).from_item(webhook)

    if _type == 'message_action':
        return MessageAction.from_item(webhook)

    if _type == 'dialog_submission':
        return DialogSubmissionAction.from_item(webhook)


def action_from_webhook(webhook):
    """
    Returns Action object from the webhook
    """
    logger.info(f"Parsing action from webhook with timestamp: {webhook['action_ts']}")
    action = get_action_from_webhook(webhook)
    logger.info(f'Parsed {action}')
    return action
