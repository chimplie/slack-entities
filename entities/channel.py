from slack.client import client, SlackNotFoundError
from slack.entities.resource import SlackResource


class Channel(SlackResource):
    def __init__(self, id, name=None, is_channel=None, **kwargs):
        self.id = id
        self.name = name
        self.is_channel = is_channel

    def __repr__(self):
        return f"<Channel {{id: '{self.id}', name: '{self.name}'}}>"

    @classmethod
    def get(cls, id=None, name=None):
        if not (id or name):
            raise ValueError("Channel parameters are not specified")

        if id:
            return super().get(id=id)
        else:
            channels = cls.filter(name=name)

            if not channels:
                raise SlackNotFoundError(f"Channel with name `{name}` does not exist")
            return channels[0]
