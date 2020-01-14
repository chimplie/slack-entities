from slack_entities.client.client import get_client
from slack_entities.entities.user import User
from .channel import Channel


class OutcomingMessage:
    """
    Describes message sent to Slack
    """
    def __init__(
        self,
        channel: Channel,
        attachments: list = None,
        text: str = '',
        token: str = None,
        blocks: list = None,
        icon_url: str = None,
        username: str = None,
        *args,
        **kwargs,
    ):
        self.channel = channel
        self.token = token
        self.text = text
        self.attachments = attachments if attachments else []
        self.blocks = blocks if blocks else []
        self.icon_url = icon_url
        self.username = username

    @property
    def message_params(self):
        params = {
            'body_encoding': 'json',
            'channel': self.channel.id,
            'text': self.text,
            'attachments': self.attachments,
            'blocks': self.blocks,
        }
        if self.icon_url is not None:
            params['icon_url'] = self.icon_url
        if self.username is not None:
            params['username'] = self.username

        return params

    def send(self):
        return get_client(token=self.token).api_call(
            'chat.postMessage',
            **self.message_params
        )

    def send_ephemeral(self, user: User):
        return get_client(token=self.token).api_call(
            'chat.postEphemeral',
            body_encoding='json',
            channel=self.channel.id,
            text=self.text,
            attachments=self.attachments,
            blocks=self.blocks,
            user=user.id
        )

    def update(self, ts):
        """
        Updates the message with the timestamp
        :param ts: Timestamp of the message to update
        """
        return get_client(token=self.token).api_call(
            'chat.update',
            ts=ts,
            **self.message_params
        )

    def send_in_thread(self, thread_ts: str):
        """ Sends threaded message.
        :param ts: Timestamp of the original parent message which thread belongs to.
        """
        return get_client(token=self.token).api_call(
            'chat.postMessage',
            thread_ts=thread_ts,
            **self.message_params
        )
