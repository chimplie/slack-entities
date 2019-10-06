from collections import Callable

from slack import RTMClient

from slack_entities.entities.event import event_from_rtm


class RTMEventClient(RTMClient):
    @staticmethod
    def run_on(*, event: str):
        """A decorator to store and link a callback to an event."""

        def decorator(callback):
            RTMEventClient.on(event=event, callback=callback)
            return callback

        return decorator

    @classmethod
    def on(cls, *, event: str, callback: Callable):
        def modified_callback(*args, **kwargs):
            event_item = kwargs.get("data", {})
            event_entity = event_from_rtm(event_item, event)
            return callback(event_entity)

        return super().on(event=event, callback=modified_callback)
