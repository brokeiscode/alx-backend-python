from datetime import datetime
import logging
from django.http import HttpResponseForbidden, JsonResponse
from django.core.cache import cache


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(message)s')

    def __call__(self, request):

        response = self.get_response(request)
        # To get authenticated user, logging is after view is called because of simple-jwt.
        user = request.user if request.user.is_authenticated else 'Anonymous'
        message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(message)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        self.current_hour = datetime.now().hour

    def __call__(self, request):

        # deny access to chat
        if 18 <= self.current_hour < 21:
            return HttpResponseForbidden(
                "Access to the messaging app is forbidden, come back between 6PM and 9PM"
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.rate_limit = 5  # Number of allowed requests
        self.time_window = 60  # Time window in seconds

        if request.method == 'POST' and '/api/conversations/' in request.path and request.path.endswith('/messages/'):
            ip = self.get_client_ip(request)
            key = f'rate-limit-{ip}'

            request_count = cache.get(key)
            if request_count is None:
                cache.set(key, 0, timeout=self.time_window)
                request_count = 0

            if request_count >= self.rate_limit:
                return JsonResponse({'error': 'Message limit exceeded.'}, status=429)

            cache.incr(key)

        response = self.get_response(request)
        return  response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/conversations/'):
            user = request.user
            if user.is_authenticated:
                role = hasattr(user, 'role')
                if role not in ['admin', 'moderator']:
                    return HttpResponseForbidden("Access denied: Admin permission required.")
                else:
                    return JsonResponse({"error": "Unauthorized request."}, status=401)

        response = self.get_response(request)

        return  response
