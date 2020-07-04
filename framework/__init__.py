from webob import Request, Response
from parse import parse
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import datetime
import inspect
import os

from .middleware import Middleware


class API:
    """Base API class for web framework"""

    def __init__(self, templates_dir="templates", static_dir=""):
        self.routes = {}
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi, root=static_dir)
        self.middleware = Middleware(self)
        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir)))

    def __call__(self, environ, start_response):
        """Get request from wsgi object with webob wrapper and return response"""
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def add_middleware(self, middleware_class):
        """Wrap app with middleware"""
        self.middleware.add(middleware_class)

    def wsgi(self, environ, start_response):
        """WSGI wrapper for whitenoise"""
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):
        """Routes decorators to associate url path and function"""

        assert path not in self.routes, f"Route '{path}' already exists"

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def render_template(self, template_name, context=None):
        """Render template with context variables"""
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        """Add custom exception to route"""
        self.exception_handler = exception_handler

    def find_handler(self, request_path):
        """Loop through saved routes and find patterns
         by comparing function path and request path"""

        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def request_info(self, request):
        """Console logger from requests"""

        user_agent = request.environ.get("HTTP_USER_AGENT")
        print(
            f"[{datetime.datetime.now()}] {request.method} '{request.path}' {user_agent}")

    def handle_request(self, request):
        """Handle request and return response to user"""

        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(
                        handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError(
                            "Method is not implemented", request.method)
                    handler(request, response, **kwargs)
                else:
                    handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        self.request_info(request)
        return response

    def default_response(self, response):
        """Not found response if page does not exists"""

        response.status_code = 404
        response.text = "Not found."

        return response
