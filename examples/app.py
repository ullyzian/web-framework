from framework import API

app = API(templates_dir="examples/templates", static_dir="examples/static")


@app.route("/home")
def home(request):
    return app.render_template(
        "index.html", context={"example": "Some sample sentence", "id": 23})


@app.route("/work/{new}")
def work(request, new):
    return f"Hello {new} work"


@app.route("/test")
class Test():
    def get(self, req, resp):
        return "New route"
