from framework import API

app = API()


@app.route("/home")
def home(request, response):
    response.body = app.render_template(
        "index.html", context={"example": "Some sample sentence", "id": 23}).encode()


@app.route("/work/{new}")
def work(request, response, new):
    response.text = f"Hello {new} work"


@app.route("/test")
class Test():
    def get(self, req, resp):
        resp.text = "New route"
