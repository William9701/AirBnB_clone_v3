from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        host = os.environ["HBNB_API_HOST"]
    else:
        host = "0.0.0.0"

    if "HBNB_API_PORT" in os.environ:
        port = os.environ["HBNB_API_PORT"]
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)