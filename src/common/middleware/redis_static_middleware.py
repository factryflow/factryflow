import redis
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RedisStaticMiddleware(MiddlewareMixin):
    """
    Middleware that caches static files in Redis.

    This middleware checks if a requested static file is already cached in Redis.
    If it is, it serves the file directly from the cache. Otherwise, it allows the
    request to proceed and caches the response in Redis if the request is successful.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis.from_url(
            settings.CACHES["default"]["LOCATION"]
        )

    def process_request(self, request):
        if request.path.startswith(settings.STATIC_URL):
            # Check Redis for cached static file
            static_file = self.redis_client.get(request.path)
            if static_file:
                return HttpResponse(
                    static_file, content_type="application/octet-stream"
                )

        return None

    def process_response(self, request, response):
        if request.path.startswith(settings.STATIC_URL) and response.status_code == 200:
            # Cache static file in Redis
            self.redis_client.set(request.path, response.content)
        return response
