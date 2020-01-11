import hashlib
import os

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

    def __eq__(self, other):
        return self.id and other.id and self.id == other.id

    def __hash__(self):
        return int(hashlib.md5(self.id.encode()).hexdigest(), 16)

    @property
    def is_public(self):
        return not self.is_private

    @classmethod
    def get_by_user_id(cls, user_id, token=None):
        """
        Creates Channel object by Slack user id (1:1 messages with bot)
        :param user_id: str
        :param token: str
        :return:
        """
        channel_id = cls.using(token)._fetch(method='im.open', return_resource='channel', user=user_id)['id']
        return cls(channel_id)

    def recent_messages(self, limit=20):
        """
        Returns recent messages in the channel
        :param limit: Limit of messages to return
        """
        messages_history_client = self.using(os.environ['CONVERSATIONS_READ_TOKEN']).client
        messages_items = messages_history_client.api_call(
            'conversations.history', channel=self.id, limit=limit)['messages']

        # Hack circular imports
        from slack_entities.entities import IncomingMessage
        return [
            IncomingMessage.from_original_message(message_item, self)
            for message_item in messages_items
        ]
