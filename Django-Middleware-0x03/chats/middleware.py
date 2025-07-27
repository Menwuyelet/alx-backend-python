import logging
from datetime import datetime, time
from django.http import HttpResponse

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s',
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request,):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info( f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
          
        self.allowed_start = time(18, 0, 0)  
        self.allowed_end = time(21, 0, 0)  
    
    def __call__(self, request):
        current_time = datetime.now().time()

        if not (self.allowed_start <= current_time <= self.allowed_end):
            return  HttpResponse(
                "Access denied: Outside of allowed chat hours (6pm to 9pm)",
                status = 403
            )
        return self.get_response