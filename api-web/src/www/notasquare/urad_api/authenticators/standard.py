from notasquare.urad_api.authenticators import BaseAuthenticator, BaseUser

# User
class User(BaseUser):
    def __init__(self):
        self.id = 0
        self.username = ''
        self.groups = []

# Authenticator
class TestAuthenticator(BaseAuthenticator):
    def parse_user(self, request):
        user = User()
        user.id = request.META['NAS-TEST-USER-ID'] if 'NAS-TEST-USER-ID' in request.META else 1
        user.username = request.META['NAS-TEST-USER-USERNAME'] if 'NAS-TEST-USER-USERNAME' in request.META else 'default'
        user.groups = ['ADMIN', 'USER']
        return user

class JWTAuthenticator(BaseAuthenticator):
    def parse_user(self, request):
        user = User()
        user.id = 1
        user.username = 'default'
        user.groups = ['DEFAULT']
        return user
