from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


# def get_user(request):
#     if not hasattr(request, '_cached_user'):
#         request._cached_user = auth.get_user(request)
#     return request._cached_user


# class AuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             session_count = request.session.get('session_count', 1)
#             request.session['session_count'] = session_count + 1
#             if not request.user.is_superuser:
#                 request.session.set_expiry(60)
#         return request.user