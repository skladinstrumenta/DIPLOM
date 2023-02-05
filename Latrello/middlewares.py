from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_count = 0
        if request.user.is_authenticated:
            session_count = request.session.get('session_count')
            if request.method == 'GET':
                session_count += 1
            if not request.user.is_superuser:
                request.session.set_expiry(60*60)
        request.session.update({'session_count': session_count})
