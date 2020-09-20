from typing import List

from slack_entities.client.client import get_client
from slack_entities.entities import Channel


class FileUpload:
    def __init__(
            self,
            channels: List[Channel],
            token: str,
            file_path: str,
            filetype: str,
            filename: str,
            initial_comment: str,
    ):
        self.channels = channels
        self.token = token
        self.filename = filename
        self.filetype = filetype
        self.initial_comment = initial_comment
        self.file_path = file_path

    @property
    def message_params(self):
        params = {
            'channels': ','.join(map(lambda c: c.id, self.channels)),
            'filename': self.filename,
            'filetype': self.filetype,
            'initial_comment': self.initial_comment
        }

        return params

    def send(self):
        return get_client(token=self.token).api_call(
            'files.upload',
            body_encoding='data',
            files={'file': self.file_path},
            **self.message_params,
        )
