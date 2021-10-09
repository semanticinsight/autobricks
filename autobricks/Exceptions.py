import enum
from .AuthFactory import AuthenticationType


class AutbricksConfigurationInvalid(Exception):
    def __init__(
        self,
        configuration_variable: str,
        value: str = None,
        valid_values: enum.Enum = None,
    ):
        self.message = f"Autobricks configuration variable '{configuration_variable}' is not valid. {configuration_variable}={value}"
        if valid_values:
            values = ", ".join([v.name for v in valid_values])
            self.message = f"{self.message}. Valid values are: {values}"
        super().__init__(self.message)


class AutbricksAuthTypeNotRegistered(Exception):
    def __init__(self, auth_type: AuthenticationType):
        self.message = f"Autobricks authentication type {auth_type} has not been registered in the AuthFactory module"
        super().__init__(self.message)
