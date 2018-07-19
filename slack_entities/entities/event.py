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

    @classmethod
    def from_item(cls, id, event_item):
        user_id = event_item.get("user") or event_item.get("bot_id")
        text = event_item["text"]
        channel_id = event_item["channel"]
        attachments = event_item.get("attachments", list())

        # Getting message object
        message = IncomingMessage(
            user_id=user_id,
            channel_id=channel_id,
            text=text,
            attachments=attachments
        )

        return cls(id, event_item=event_item, message=message)


class EventFactory:
    mapping_rules = {
        'message': MessageEvent
    }
    default_class = Event

    def get_class(self, event_type) -> Event:
        """
        Returns class that should be used for the event
        """
        return self.mapping_rules.get(event_type) or self.default_class

    def from_item(self, id, event_item):
        """
        Returns event by its id and item
        """
        event_class = self.get_class(event_item['type'])
        return event_class.from_item(id, event_item)

    def from_webhook(self, webhook):
        """
        Exstracts event from the webhook
        """
        event_id = webhook["event_id"]
        event_item = webhook['event']

        return self.from_item(event_id, event_item)


factory = EventFactory()


def event_from_webhook(webhook) -> Event:
    """
    Returns Event object from the webhook
    """
    logger.info(f"Parsing event from webhook with id: {webhook['event_id']}")
    event = factory.from_webhook(webhook)
    logger.info(f"Parsed {event}")
    return event
