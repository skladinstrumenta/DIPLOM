from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone

from django.conf import settings


class TokenExpiredAuthentication(TokenAuthentication):
    def authenticate(self, request):
        authenticate = super().authenticate(request)
        if authenticate:
            user, token = authenticate
        else:
            return authenticate
        # if (timezone.now() - token.created).seconds > settings.TOKEN_LIFE:
        #     token.delete()
        #
        #     msg = "Your Token has died, please generate a new one!"
        #     raise exceptions.AuthenticationFailed(msg)
        return user, token
