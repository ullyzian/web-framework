import os


def quickstart():
    os.mkdir("templates")
    os.mkdir("static")

    start = """from framework import API\n\napp = API()\n\n@app.route("/hello-world")\ndef hello_world(request):\n\treturn "<h1>Hello world</h1>" """

    with open("app.py", "w") as f:
        f.write(start)


if __name__ == "__main__":
    quickstart()
