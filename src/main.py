from flask import Flask, render_template, request
from handler import proxy
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video/<string:vid>.<any(jpg,webp):ext>")
def image(vid, ext):
    return proxy.image(vid, ext)


@app.route("/video/api/v3/videos")
def videos():
    return proxy.videos(request.args, {"part": "id,snippet,contentDetails,statistics"})


@app.route("/video/api/v3/search")
def search():
    return proxy.search(request.args, {"part": "id,snippet"})


@app.route("/video/api/v3/channels")
def channels():
    return proxy.channels(request.args, {"part": "id,snippet,contentDetails,statistics"})


@app.route("/video/api/v3/playlists")
def playlists():
    return proxy.playlists(request.args, {"part": "id,snippet"})


@app.route("/video/api/v3/playlistItems")
def playlistItems():
    return proxy.playlistItems(request.args, {"part": "id,snippet,contentDetails"})


@app.route("/video/api/v3/categories")
def categories():
    return proxy.categories(request.args, {"part": "id,snippet"})


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html")


@app.errorhandler(500)
def server_error(error):
    return str(error), 500, {"Content-Type": "text/plain"}


@app.after_request
def apply_caching(response):
    if response.status == 200:
        response.headers["Cache-Control"] = "public, max-age=86400"
    return response


if __name__ == "__main__":
    app.run()
