from .channel import Channel
from .user import User


class IncomingMessage:
    """
    Describes message got from Slack
    """
    _user: User = None
    _channel: Channel = None

    def __init__(self, user_id: str, channel_id: str, text: str, attachments: list):
        self._user_id = user_id
        self._channel_id = channel_id
        self.text = text
        self.attachments = attachments

    def user(self, token=None) -> User:
        if not self._user:
            self._user = User.using(token).get(id=self._user_id)

        return self._user

    def channel(self, token=None) -> Channel:
        if not self._channel:
            self._channel = Channel.using(token).get(id=self._channel_id)

        return self._channel
