from async_timeout import timeout
from django.core.cache import cache
from .views import LIVE_FOREVER

class PasteAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        curr = cache.get('total-hits') or 0

        cache.set('total-hits', curr + 1, timeout=LIVE_FOREVER)
        
        if request.method == 'GET':
            # extract key
            request_path = request.path
            tokens = request_path.split('/')
            tokens = [x for x in tokens if x != '']

            if len(tokens) == 2:
                key = tokens[1]
                
                view_count_key = f'{key}-view-count'
                view_count = cache.get(view_count_key) or 0

                cache.set(view_count_key, view_count + 1, timeout=LIVE_FOREVER)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
