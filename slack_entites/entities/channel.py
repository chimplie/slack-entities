from .resource import SlackResource


class Channel(SlackResource):
    def __init__(self, id, name=None, is_channel=None, **kwargs):
        self.id = id
        self.name = name
        self.is_channel = is_channel

    def __repr__(self):
        return f"<Channel #{self.name}>"

    @property
    def is_direct(self):
        return self.id.startswith("D")

    @property
    def is_public(self):
        return self.id.startswith("C")
