from .. import app


@app.route('/')
def home():
    return 'Hello, go to /swagger to see how API works'
