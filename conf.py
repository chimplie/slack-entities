from appconf import AppConf

from bot.settings import SLACK_BOT_TOKEN, SLACK_TOKEN


class SlackConf(AppConf):
    BOT_TOKEN = SLACK_BOT_TOKEN
    TOKEN = SLACK_TOKEN
