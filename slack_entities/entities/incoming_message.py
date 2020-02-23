from slack.web.classes.blocks import SectionBlock, DividerBlock, ActionsBlock
from slack.web.classes.elements import ButtonElement

from .team import Team
from .channel import Channel
from .user import User


class IncomingMessage:
    """
    Describes message got from Slack
    """
    _user: User = None
    _channel: Channel = None
    _team: Team = None

    def __init__(
        self,
        user_id: str,
        channel_id: str,
        team_id: str,
        text: str,
        attachments: list = [],
        blocks: list = None,
        ts: str = None
    ):
        self._user_id = user_id
        self._channel_id = channel_id
        self._team_id = team_id
        self.text = text
        self.attachments = attachments
        self.blocks = blocks
        self.ts = ts

    def user(self, token=None) -> User:
        if not self._user:
            self._user = User.using(token).get(id=self._user_id)

        return self._user

    def channel(self, token=None) -> Channel:
        if not self._channel:
            self._channel = Channel.using(token).get(id=self._channel_id)

        return self._channel

    def team(self) -> Team:
        if not self._team:
            self._team = Team(id=self._team_id)

        return self._team

    @classmethod
    def from_item(cls, webhook):
        original_message = webhook['message']

        return cls.from_original_message(original_message, channel_id=webhook['channel']['id'])

    @classmethod
    def from_original_message(cls, original_message, channel=None, channel_id=None):
        channel_id = channel_id or channel and channel.id
        if not channel_id:
            raise ValueError("Neither `channel` nor `channel_id` is specified.")

        return cls(
            user_id=original_message.get('user') or original_message.get('bot_id'),
            channel_id=channel_id,
            text=original_message['text'],
            attachments=original_message.get('attachments', []),
            blocks=cls._transform_blocksjson_to_classes(original_message.get('blocks', [])),
            ts=original_message.get('ts'),
            team_id=original_message.get("team"),
        )

    @classmethod
    def _transform_blocksjson_to_classes(cls, blocks: list) -> list:
        result = []

        for block in blocks:
            if block['type'] == 'divider':
                result.append(DividerBlock())
            elif block['type'] == 'section':
                result.append(cls._get_section_object(block))
            elif block['type'] == 'actions':
                result.append(cls._get_actions_block(block))

        return result

    @classmethod
    def _get_section_object(cls, block: dict) -> SectionBlock:
        result = {
            'text': block.get('text', {}).get('text', ''),
            # TODO Figure out where we can get 'block_id'
            'block_id': block.get('block_id'),
        }

        accessory_object = block.get('accessory', {})

        # Currently we support only 'button' type for accessory
        if accessory_object.get('type', '') == 'button':
            button_element = ButtonElement(
                text=accessory_object.get('text', {}).get('text', ''),
                # TODO Figure out where we can get 'action_id'
                action_id=accessory_object.get('action_id', ''),
                value=accessory_object.get('value', '')
            )

            if accessory_object.get('style'):
                button_element.style = accessory_object.get('style')

            result['accessory'] = button_element

        # Removing keys with empty values
        result = {k: v for k, v in result.items() if v}
        return SectionBlock(**result) if result else None

    @classmethod
    def _get_actions_block(cls, block: dict) -> ActionsBlock:
        result = []

        for element in block.get('elements', []):
            # Currently we support only 'button' type for element
            if element.get('type') == 'button':
                result.append(ButtonElement(
                    text=element.get('text', {}).get('text', ''),
                    # TODO Figure out where we can get 'action_id'
                    action_id=element.get('action_id', ''),
                    value=element.get('value', '')
                ))

        return ActionsBlock(elements=result, block_id=block.get('block_id')) if result else None
