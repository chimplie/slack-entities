from slack_entities.client.client import get_client


class Dialog:
    """
    Describes dialog sent to Slack
    """
    def __init__(self, dialog: dict, trigger_id: str, token: str=None):
        self.token = token
        self.dialog = dialog
        self.trigger_id = trigger_id

    def send(self):
        return get_client(token=self.token).api_call(
            'dialog.open',
            body_encoding='json',
            dialog=self.dialog,
            trigger_id=self.trigger_id
        )
