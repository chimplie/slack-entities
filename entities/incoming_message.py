from slack.entities.channel import Channel
from slack.entities.user import User


class IncomingMessage:
    """
    Describes message sent in Slack
    """
    _user: User
    _channel: Channel

    def __init__(
            self,
            user_id: str,
            channel_id: str,
            text: str,
            attachments: list=list()
        ):
        self._user_id = user_id
        self._channel_id = channel_id
        self.text = text
        self.attachments = attachments

    @property
    def user(self) -> User:
        if not self._user:
            self._user = User.get(id=self._user_id)

        return self._user

    @property
    def channel(self) -> Channel:
        if not self._channel:
            self._channel = Channel.get(id=self._channel_id)

        return self._channel
