from flask import Flask, request, make_response
from dotenv import load_dotenv

import os

from ig_crawler import crawl_ig

load_dotenv()

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['JSON_AS_ASCII'] = False

@app.route("/profile/<path:username>", methods=['GET'])
def get_profile(username):
    data = crawl_ig(username)
    data.pop("new_posts")
    return make_response(data, 200)

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)