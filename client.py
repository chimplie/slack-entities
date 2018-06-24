import logging

from slackclient import SlackClient

from django.conf import settings


logger = logging.Logger("slack_client", level=15)
logger.setLevel(15)


class SlackApiError(Exception):
    pass


class SlackNotFoundError(Exception):
    pass


class SlackClientWithLogging(SlackClient):
    def api_call(self, method, timeout=None, **kwargs):
        logger.info(f"Fetching `{method}` with params `{kwargs}`")
        response = super().api_call(method, timeout, **kwargs)
        logger.info(f"Response:\n {response}")
        return response


client = SlackClientWithLogging(settings.SLACK_BOT_TOKEN)
