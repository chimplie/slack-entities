import logging

from slack.entities.incoming_message import IncomingMessage


logger = logging.getLogger("event_factory")


class Event:
    """
    Represents slack event
    """
    def __init__(self, id, payload):
        self.id = id
        self.payload = payload
        self.subtype = payload.get("subtype")

    @classmethod
    def from_item(cls, id, payload):
        return cls(id, payload)

    def __repr__(self):
        return f"<{self.__class__.__name__} {{id: {self.id}}}>"


class MessageEvent(Event):
    def __init__(self, id, payload, message: IncomingMessage):
        super().__init__(id, payload)
        self.message = message
        self.payload = payload

    @classmethod
    def from_item(cls, id, item):
        user_id = item.get("user") or item.get("bot_id")
        text = item["text"]
        channel_id = item["channel"]
        attachments = item.get("attachments")

        # Getting message object
        message = IncomingMessage(
            user_id=user_id,
            channel_id=channel_id,
            text=text,
            attachments=attachments
        )

        return cls(id, payload=item, message=message)


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

    def from_item(self, id, item):
        """
        Returns event by its id and item
        """
        event_class = self.get_class(item['type'])
        return event_class.from_item(id, item)

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
