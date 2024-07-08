# movie_app/middleware.py

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['request_count'] = request.session.get('request_count', 0) + 1
        response = self.get_response(request)
        return response