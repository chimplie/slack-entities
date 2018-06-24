from slack.entities.message import Message


class Event:
    """
    Represents slack event
    """
    def __init__(self, id):
        self.id = id

    @classmethod
    def from_item(cls, id, item):
        raise NotImplementedError


class MessageEvent(Event):
    def __init__(self, id,  message: Message):
        super().__init__(id)
        self.message = message

    @classmethod
    def from_item(cls, id, item):
        user_id = item.get("user") or item.get("bot_id")
        text = item["text"]
        channel_id = item["channel"]
        attachments = item.get("attachments")

        # Getting message object
        message = Message(
            user_id=user_id,
            channel_id=channel_id,
            text=text,
            attachments=attachments
        )

        return cls(id, message)
