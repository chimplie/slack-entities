from slack_entities.client.client import get_client
from .channel import Channel


class OutcomingMessage:
    def __init__(self, channel: Channel, attachments: list=None, text: str='', token: str=None):
        self.channel = channel
        self.token = token
        self.text = text
        self.attachments = attachments if attachments is None else []

    def send(self):
        get_client(token=self.token).api_call(
            'chat.postMessage',
            channel=self.channel.id,
            text=self.text,
            attachments=self.attachments
        )
