from slack.client import client
from slack.entities.channel import Channel


class OutcomingMessage:
    def __init__(self, channel: Channel, text: str, attachments: list):
        self.channel = channel
        self.text = text
        self.attachments = attachments

    def send(self):
        client.api_call(
            'chat.postMessage',
            channel=self.channel.id,
            text=self.text,
            attachments=self.attachments
        )
