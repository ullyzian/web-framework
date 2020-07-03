from framework.api import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello home"


@app.route("/work")
def work(request, response):
    response.text = "Hello work"
