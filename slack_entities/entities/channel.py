from .resource import SlackResource


class Channel(SlackResource):
    fetch_api_method = "conversations.info"
    fetch_all_api_method = "conversations.list"

    def __init__(self, id, name=None, is_channel=None, is_im=None, is_private=None, is_group=None, **kwargs):
        self.id = id
        self.name = name
        self.is_channel = is_channel
        self.is_direct = is_im
        self.is_private = is_private
        self.is_group = is_group

    def __repr__(self):
        return f"<Channel #{self.name or self.id}>"

    @property
    def is_public(self):
        return not self.is_private
