
# Authenticator
class AbstractAuthenticator(object):
    def parse_user(self, params):
        pass

class BaseAuthenticator(AbstractAuthenticator):
    pass

# User
class AbstractUser(object):
    pass

class BaseUser(AbstractUser):
    pass

# Import common implement
import standard
