import logging
import os

from slackclient import SlackClient


logger = logging.Logger("slack_client", level=15)
logger.setLevel(15)


class SlackApiError(Exception):
    pass


class SlackNotFoundError(Exception):
    pass


class NoSlackTokenError(Exception):
    pass


class SlackClientWithLogging(SlackClient):
    def api_call(self, method, timeout=None, **kwargs):
        logger.info(f"Fetching `{method}` with params `{kwargs}`")
        response = super().api_call(method, timeout, **kwargs)
        logger.info(f"Response:\n {response}")
        return response


def get_client(token=None):
    # Trying to get token from environment
    if not token:
        token = os.environ.get("SLACK_TOKEN")

    # If there is still no token - it's bad.
    # Need to raise appropriate error
    if not token:
        raise NoSlackTokenError(
            """You need to set Slack token. You can do this in the following ways:
            1) set up a 'SLACK_TOKEN' environment variable
            2) directly pass Slack token into get_client() function""")

    return SlackClientWithLogging(token=token)
