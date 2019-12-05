from typing import List, Optional, Union

from slack_entities.client.client import get_client
from slack.web.classes.blocks import Block
from slack.web.classes.objects import extract_json


def str_to_slack_text_element(attr: Union[str, dict], text_type: Optional[str] = 'plain_text') -> dict:
    if isinstance(attr, str):
        return {
            'type': text_type,
            'text': attr,
        }
    return attr


class View:
    """
    Basic class for different types of views.
    """
    _type = None

    def __init__(
        self,
        trigger_id: str,
        callback_id: str,
        title: str,
        blocks: List[Block],
        submit: Optional[str] = 'Submit',
        close: Optional[str] = 'Close',
        token: Optional[str] = None
    ):
        self.token = token
        self.trigger_id = trigger_id
        self.callback_id = callback_id
        self._title = title
        self._blocks = blocks
        self._close = close
        self._submit = submit

    def open(self):
        return get_client(self.token).api_call(
            'views.open',
            body_encoding='json',
            trigger_id=self.trigger_id,
            view=self.view
        )

    @property
    def view(self):
        return {
            'type': self._type,
            'title': self.title,
            'blocks': self.blocks,
            'close': self.close,
            'submit': self.submit,
            'callback_id': self.callback_id,
        }

    @property
    def blocks(self):
        return extract_json(self._blocks)

    @property
    def title(self):
        return str_to_slack_text_element(self._title)

    @property
    def submit(self):
        return str_to_slack_text_element(self._submit)

    @property
    def close(self):
        return str_to_slack_text_element(self._close)


class Modal(View):
    _type = 'modal'
