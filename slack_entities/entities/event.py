import logging

from .incoming_message import IncomingMessage


logger = logging.getLogger("event_factory")


class Event:
    """
    Represents slack-entities-entities event
    """
    def __init__(self, id, event_item):
        self.id = id
        self.event_item = event_item
        self.subtype = event_item.get("subtype")

    @classmethod
    def from_item(cls, id, event_item):
        return cls(id, event_item)

    def __repr__(self):
        return f"<{self.__class__.__name__} {{id: {self.id}}}>"


class MessageEvent(Event):
    def __init__(self, id, event_item, message: IncomingMessage):
        super().__init__(id, event_item)
        self.message = message

    @staticmethod
    def parse_message(event_item):
        return IncomingMessage(
            user_id=event_item.get("user") or event_item.get("bot_id"),
            channel_id=event_item["channel"],
            text=event_item["text"],
            attachments=event_item.get("attachments", list())
        )

    @classmethod
    def from_item(cls, id, event_item):
        return cls(id, event_item=event_item, message=cls.parse_message(event_item))


class EditedMessageEvent(MessageEvent):
    def __init__(self, id, event_item, message: IncomingMessage, previous_message: IncomingMessage):
        super().__init__(id, event_item, message)
        self.previous_message = previous_message

    @classmethod
    def from_item(cls, id, event_item):
        return cls(
            id,
            event_item=event_item,
            message=IncomingMessage(
                user_id=event_item['message'].get("user") or event_item.get("bot_id"),
                channel_id=event_item["channel"],
                text=event_item['message']["text"],
                attachments=event_item['message'].get("attachments", list())
            ),
            previous_message=IncomingMessage(
                user_id=event_item['previous_message'].get("user") or event_item.get("bot_id"),
                channel_id=event_item["channel"],
                text=event_item['previous_message']["text"],
                attachments=event_item['previous_message'].get("attachments", list())
            )
        )


class EventFactory:
    def get_class(self, event):
        """
        Returns class that should be used for the event
        """
        if event.get('subtype') == 'message_changed' and event.get('type') == 'message':
            return EditedMessageEvent

        if event.get('type') == 'message':
            return MessageEvent

        return Event

    def from_item(self, id, event_item):
        """
        Returns event by its id and item
        """
        event_class = self.get_class(event_item)
        return event_class.from_item(id, event_item)

    def from_webhook(self, webhook):
        """
        Exstracts event from the webhook
        """
        event_id = webhook["event_id"]
        event_item = webhook['event']

        return self.from_item(event_id, event_item)


factory = EventFactory()


def event_from_webhook(webhook):
    """
    Returns Event object from the webhook
    """
    logger.info(f"Parsing event from webhook with id: {webhook['event_id']}")
    event = factory.from_webhook(webhook)
    logger.info(f"Parsed {event}")
    return event
