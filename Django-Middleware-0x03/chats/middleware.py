from datetime import datetime
import logging
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(message)s')

    def __call__(self, request):

        response = self.get_response(request)
        # To get authenticated user, logging is after view called.
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