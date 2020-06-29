from typing import Optional
import logging
import os

from slack import WebClient


SLACK_ENTITIES_LOGGER_LEVEL = int(os.environ.get('SLACK_ENTITIES_LOGGER_LEVEL', 15))
logger = logging.Logger("slack_client", level=SLACK_ENTITIES_LOGGER_LEVEL)
logger.setLevel(SLACK_ENTITIES_LOGGER_LEVEL)


class SlackApiError(Exception):
    pass


class SlackNotFoundError(Exception):
    pass


class NoSlackTokenError(Exception):
    pass


class SlackClientWithLogging(WebClient):
    def api_call(self, api_method: str, body_encoding: Optional[str] = 'data', **kwargs):
        logger.info(f"Fetching `{api_method}` with params `{kwargs}`")

        params = {'api_method': api_method}
        # Some methods require body to be sent as data and some - as json.
        # We send it as data by default.
        params[body_encoding] = kwargs

        response = super().api_call(**params)
        logger.info(f"Response: {response.status_code}.")
        return response


def get_client(token: str = None):
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
