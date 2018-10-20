from slack_entities.entities.resource import SlackResource
from slack_entities.exceptions.exceptions import PluralMethodError


class Team(SlackResource):
    fetch_api_method = 'team.info'

    def __init__(
            self,
            id,
            name=None,
            enterprise_id=None,
            enterprise_name=None,
            domain=None,
            email_domain=None,
            **kwargs
    ):
        self.id = id
        self.name = name
        self.enterprise_id = enterprise_id
        self.enterprise_name = enterprise_name
        self.domain = domain
        self.email_domain = email_domain

    def __repr__(self):
        return f"<Team #{self.name or self.id}>"

    @classmethod
    def _get_name_plural(cls):
        """
        For Team entity there is no plural name
        """
        raise PluralMethodError

    @classmethod
    def _get_fetch_all_method(cls):
        """
        For Team entity there is no plural method
        """
        raise PluralMethodError

    @classmethod
    def get(cls, **kwargs):
        """
        Returns single object by specified parameters
        """
        return cls.from_item(cls._fetch(**kwargs))

    @classmethod
    def filter(cls, **kwargs):
        """
        We can't use filter
        """
        raise PluralMethodError
