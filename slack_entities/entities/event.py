import logging

from slack_entities.entities.user import User
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
            attachments=event_item.get("attachments", list()),
            team_id=event_item.get("team"),
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
                attachments=event_item['message'].get("attachments", list()),
                team_id=event_item.get("team"),
            ),
            previous_message=IncomingMessage(
                user_id=event_item['previous_message'].get("user") or event_item.get("bot_id"),
                channel_id=event_item["channel"],
                text=event_item['previous_message']["text"],
                attachments=event_item['previous_message'].get("attachments", list()),
                team_id=event_item.get("team"),
            )
        )


class DeletedMessageEvent(MessageEvent):
    def __init__(self, id, event_item, message: IncomingMessage):
        super().__init__(id, event_item, message)

    @classmethod
    def from_item(cls, id, event_item):
        return cls(
            id,
            event_item=event_item,
            message=IncomingMessage(
                user_id=event_item['previous_message'].get("user") or event_item.get("bot_id"),
                channel_id=event_item["channel"],
                text=event_item['previous_message']["text"],
                attachments=event_item['previous_message'].get("attachments", list()),
                team_id=event_item.get("team"),
            )
        )


class BotMessageEvent(MessageEvent):
    @classmethod
    def from_item(cls, id, event_item):
        return cls(
            id,
            event_item=event_item,
            message=IncomingMessage(
                user_id=event_item.get("bot_id"),
                channel_id=event_item["channel"],
                text=event_item["text"],
                team_id=event_item.get("team"),
            )
        )


class UserChangeEvent(Event):
    def __init__(self, id, event_item, user: User):
        super().__init__(id, event_item)
        self.user = user

    @classmethod
    def from_item(cls, id, event_item):
        return cls(
            id, event_item,
            user=User.from_item(event_item['user'])
        )


class TeamJoinEvent(Event):
    def __init__(self, id, event_item, user: User):
        super().__init__(id, event_item)
        self.user = user

    @classmethod
    def from_item(cls, id, event_item):
        return cls(
            id, event_item,
            user=User.from_item(event_item['user'])
        )


class EventFactory:
    def get_class(self, event):
        """
        Returns class that should be used for the event
        """
        if event.get('subtype') == 'message_changed' and event.get('type') == 'message':
            return EditedMessageEvent

        if event.get('subtype') == 'message_deleted' and event.get('type') == 'message':
            return DeletedMessageEvent

        if event.get('subtype') == 'bot_message' and event.get('type') == 'message':
            return BotMessageEvent

        # For new apps slack sends different message structure for bot users.
        if event.get('bot_id') is not None and event.get('type') == 'message':
            return BotMessageEvent

        if event.get('type') == 'message':
            return MessageEvent

        if event.get('type') == 'user_change':
            return UserChangeEvent

        if event.get('type') == 'team_join':
            return TeamJoinEvent

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

    def from_rtm_event(self, id, event_type, data):
        data['type'] = event_type

        return self.from_item(id, data)


factory = EventFactory()


def event_from_webhook(webhook):
    """
    Returns Event object from the webhook
    """
    logger.info(f"Parsing event from webhook with id: {webhook['event_id']}")
    event = factory.from_webhook(webhook)
    logger.info(f"Parsed {event}")
    return event


def event_from_rtm(rtm_event: dict, event_type: str):
    id = rtm_event['event_ts']
    logger.info(f"Parsing event from RTM event with id: {id}")

    event = factory.from_rtm_event(id, event_type, rtm_event)
    logger.info(f"Parsed {event}")
    return event
