from slack.web.classes.blocks import Block

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
        attachments: list = None,
        blocks: list = None,
        ts: str = None
    ):
        self._user_id = user_id
        self._channel_id = channel_id
        self._team_id = team_id
        self.text = text
        self.attachments = attachments if attachments else []
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
            blocks=Block.parse_all(original_message.get('blocks', [])),
            ts=original_message.get('ts'),
            team_id=original_message.get("team"),
        )
