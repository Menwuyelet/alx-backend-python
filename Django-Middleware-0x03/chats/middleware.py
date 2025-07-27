import logging
from datetime import datetime, time
from django.http import HttpResponse
from collections import defaultdict, deque

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
        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_request):
        self.get_response = get_request
        self.message_log = defaultdict(deque)
        self.limit = 5  
        self.time_window = 60 

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.message_log[ip]

            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            if len(timestamps) >= self.limit:
                return HttpResponse(
                    "Rate limit exceeded: Max 5 messages per minute allowed.",
                    status=429
                )   
            timestamps.append(now)
        return self.get_response(request)    


## ip request
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get("REMOTE_ADDR", "") 