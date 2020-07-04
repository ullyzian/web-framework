from webob import Request


class Middleware:
    """
    Middleware base class

    Example:

    class CustomMiddleware(Middleware):
        def process_request(self, request):
            # do stuff

        def process_response(self, request, response):
            # do stuff
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """WSGI request entrypoint"""
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_class):
        """Add middleware wrapper"""
        self.app = middleware_class(self.app)

    def process_request(self, request):
        """Function to implement request processing"""
        pass

    def process_response(self, request, response):
        """Function to implement response processing"""
        pass

    def handle_request(self, request):
        """Handle request"""
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response
