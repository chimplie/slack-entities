import logging
import os

from slack import WebClient

logger = logging.Logger("slack_client", level=15)
logger.setLevel(15)


class SlackApiError(Exception):
    pass


class SlackNotFoundError(Exception):
    pass


class NoSlackTokenError(Exception):
    pass


class SlackClientWithLogging(WebClient):
    def api_call(self, api_method, **kwargs):
        logger.info(f"Fetching `{api_method}` with params `{kwargs}`")

        params = {'api_method': api_method}
        # We have to use json instead of data to send blocks.
        if 'chat' in api_method:
            params['json'] = kwargs
        else:
            params['data'] = kwargs

        response = super().api_call(**params)
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
