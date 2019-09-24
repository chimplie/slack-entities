from slack_entities.client.client import get_client
from slack_entities.entities.user import User
from .channel import Channel


class OutcomingMessage:
    """
    Describes message sent to Slack
    """
    def __init__(self, channel: Channel, attachments: list=None, text: str='', token: str=None, blocks: list=None):
        self.channel = channel
        self.token = token
        self.text = text
        self.attachments = attachments if attachments else []
        self.blocks = blocks if blocks else []

    def send(self):
        return get_client(token=self.token).api_call(
            'chat.postMessage',
            channel=self.channel.id,
            text=self.text,
            attachments=self.attachments,
            blocks=self.blocks,
        )

    def send_ephemeral(self, user: User):
        return get_client(token=self.token).api_call(
            'chat.postEphemeral',
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
            channel=self.channel.id,
            ts=ts,
            text=self.text,
            attachments=self.attachments,
            blocks=self.blocks,
        )
