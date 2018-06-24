from django.apps import AppConfig


class SlackConfig(AppConfig):
    name = 'slack'

    def ready(self):
        # Imports below are necessary
        from slack.conf import SlackConf
        # ^^^^
