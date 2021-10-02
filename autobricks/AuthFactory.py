from enum import Enum
from .Auth import (
    UserAuth,
    SPAuth,
    SPMgmtEndpointAuth
)

class AuthenticationType(Enum):

    USER = 1,
    SERVICE_PRINCIPLE = 2,
    SERVICE_PRINCIPLE_MGMT_ENDPOINT = 3


class AuthFactory:

    def __init__(self):
        self._creators = {}

    def register_format(self, auth_type: AuthenticationType, creator: type):
        self._creators[auth_type] = creator

    def get_auth(self, auth_type: AuthenticationType, parameters:dict):

        creator = self._creators.get(auth_type)
        if not creator:
            raise ValueError(auth_type)

        return creator(parameters)


auth_factory = AuthFactory()
auth_factory.register_format(AuthenticationType.USER, UserAuth)
auth_factory.register_format(AuthenticationType.SERVICE_PRINCIPLE, SPAuth)
auth_factory.register_format(AuthenticationType.SERVICE_PRINCIPLE_MGMT_ENDPOINT, SPMgmtEndpointAuth)
