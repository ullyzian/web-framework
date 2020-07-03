import pytest

from api import API


@pytest.fixture
def api():
    return API()


def test_basic_route(api):
    @api.route("/test")
    def test(req, resp):
        resp.text = "Test"

    with pytest.raises(AssertionError):
        @api.route("/test")
        def test2(req, resp):
            resp.text = "Diplicate route"


def test_route_parametrs(api):
    @api.route("/test/{number}")
    def test(req, resp, number):
        resp.text = f"Parametr: {number}"


def test_class_route(api):
    @api.route("/url")
    class Test:
        def get(self, req, resp):
            resp.text = "Hello"

    @api.route("/url/{number}")
    class Test2:
        def get(self, req, resp, number):
            resp.text = f"URL number: {number}"
