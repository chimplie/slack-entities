from datetime import timedelta

from .resource import SlackResource


class UserProfile(SlackResource):
    def __init__(
            self,
            title: str,
            phone: str,
            real_name: str,
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            image_original: str = None,
            status_text_canonical: str = None,
            **kwargs
    ):
        self.title = title,
        self.phone = phone
        self.real_name = real_name
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.image_original = image_original
        self.status_text_canonical = status_text_canonical

    def __repr__(self):
        return f"<UserProfile of {self.real_name}>"


class User(SlackResource):
    """
    Represents Slack User
    """
    resource_name_plural = "members"
    fetch_api_method = "users.info"
    fetch_all_api_method = "users.list"

    def __init__(
            self,
            id: str,
            name: str,
            deleted: bool = None,
            tz_offset: float = None,
            profile: UserProfile = None,
            is_admin: bool = None,
            is_owner: bool = None,
            is_primary_owner: bool = None,
            is_restricted: bool = None,
            is_ultra_restricted: bool = None,
            is_bot: bool = None,
            is_app_user: bool = None,
            real_name: str = None,
            **kwargs
    ):
        self.id = id
        self.name = name
        self.deleted = deleted
        if tz_offset:
            self.timezone = timedelta(seconds=tz_offset)
        else:
            self.timezone = None
        self.profile = profile
        self.is_admin = is_admin
        self.is_owner = is_owner
        self.is_primary_owner = is_primary_owner
        self.is_restricted = is_restricted
        self.is_ultra_restricted = is_ultra_restricted
        self.is_bot = is_bot
        self.is_app_user = is_app_user
        self.real_name = real_name

    def __repr__(self):
        return f"<User @{self.name}>"

    @classmethod
    def from_item(cls, item):
        # Converting Profile to object
        item['profile'] = UserProfile.from_item(item['profile'])

        return super().from_item(item)
