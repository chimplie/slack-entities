from slack_entities.client.client import get_client, SlackApiError, SlackClient, NoSlackTokenError


def get_default_client():
    try:
        return get_client()
    except NoSlackTokenError:
        return None


class SlackResource:
    """
    Base class for the any Slack resource
    """
    id: str
    resource_name: str = None
    resource_name_plural: str = None
    fetch_api_method: str = None
    fetch_all_api_method: str = None
    client: SlackClient = get_default_client()

    def __repr__(self):
        return f"<{self.resource_name} {self.id}>"

    @classmethod
    def using(cls, token):
        cls.client = get_client(token=token)
        return cls

    @classmethod
    def _get_name(cls):
        return cls.resource_name or cls.__name__.lower()

    @classmethod
    def _get_name_plural(cls):
        return cls.resource_name_plural or f"{cls._get_name()}s"

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def _get_fetch_method(cls):
        """
        Default fetch method
        """
        # Channel - channels.info
        # Team - team.info
        # User - users.info
        # Message - ?
        return cls.fetch_api_method or f"{cls._get_name_plural()}.info"

    @classmethod
    def _get_fetch_all_method(cls):
        """
        Fetch method for the all objects
        :return:
        """
        # Channel - channels.list OR conversations.list
        # Team - DOESN'T EXIST !!!
        # User - users.list
        # Message - im.list
        return cls.fetch_all_api_method or f"{cls._get_name_plural()}.list"

    @classmethod
    def from_item(cls, item):
        """
        Create SlackResource-like class object
        :param item: dict
        :return:
        """
        return cls(**item)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns single object by specified parameters
        """
        # Rename `id` to resource name for the Slack API
        if 'id' in kwargs:
            kwargs[cls._get_name()] = kwargs.pop('id')
            item = cls._fetch(**kwargs)
            return cls.from_item(item)
        else:
            resources = cls.filter(**kwargs)
            if len(resources) > 1:
                raise SlackApiError(f"Multiple {cls._get_name_plural()} with params {kwargs} exists.")
            elif len(resources) == 0:
                raise SlackApiError(f"There is no {cls._get_name_plural()} with params {kwargs}.")
            return resources[0]

    @classmethod
    def all(cls):
        """
        Returns all available objects from Slack API
        """
        items = cls._fetch_all()
        all = []

        for item in items:
            all.append(cls.from_item(item))

        return all

    @classmethod
    def filter(cls, **kwargs):
        """
        Filters resources by specified parameters
        """
        all_ = cls.all()

        return list(filter(
            lambda r: all(
                r.__getattribute__(attr) == value for attr, value in kwargs.items()
            ),
            all_
        ))

    @classmethod
    def _fetch_all(cls, method=None, return_resources=None, **kwargs):
        return cls._fetch(
            method=method or cls._get_fetch_all_method(),
            return_resource=return_resources or cls._get_name_plural(),
            **kwargs
        )

    @classmethod
    def _fetch(cls, method=None, return_resource=None, **kwargs):
        assert cls.client, f"""Slack {cls._get_name().capitalize()} API client is not specified.
        Use .set_client() method or pass token using environment variable "SLACK_TOKEN"
        """

        method = method or cls._get_fetch_method()

        response = cls.client.api_call(method, **kwargs)

        if not response["ok"]:
            raise SlackApiError(response['error'])

        return response[return_resource or cls._get_name()]
