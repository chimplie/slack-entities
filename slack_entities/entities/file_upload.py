from typing import List

from slack_entities.client.client import get_client
from slack_entities.entities import Channel


class FileUpload:
    def __init__(
            self,
            channels: List[Channel],
            token: str,
            content: bytes,
            filetype: str = None,
            filename: str = None,
            initial_comment: str = None,
    ):
        self.channels = channels
        self.token = token
        self.content = content
        self.filename = filename
        self.filetype = filetype
        self.initial_comment = initial_comment

    @property
    def message_params(self):
        params = {
            'channels': ','.join(map(lambda c: c.id, self.channels)),
            'content': self.content,
            'filename': self.filename,
            'filetype': self.filetype,
            'initial_comment': self.initial_comment
        }

        return params

    def send(self):
        return get_client(token=self.token).api_call(
            'files.upload',
            body_encoding='json',
            **self.message_params
        )
