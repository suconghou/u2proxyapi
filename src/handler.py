from urllib import urlencode
import req
import os


class proxy():

    key = os.environ.get("YOUTUBE_API_KEY")

    api = 'https://www.googleapis.com/youtube/v3/{}'

    imageMap = {
        "jpg": "http://i.ytimg.com/vi/",
        "webp": "http://i.ytimg.com/vi_webp/"
    }

    @classmethod
    def fetch(cls, url, args, params):
        params["key"] = cls.key
        argdict = args.to_dict()
        query = dict(argdict.items() + params.items())
        q = query.get('q')
        if q:
            query['q'] = q.encode('utf-8').strip()
        qs = urlencode(query)
        return req.fetch("{}?{}".format(url, qs))

    @classmethod
    def json(cls, url, args, params):
        try:
            data = cls.fetch(url, args, params)
            return data, 200, {"Content-Type": "application/json", "Cache-Control": "public, max-age=604800"}
        except Exception as e:
            return str(e), 500, {"Content-Type": "text/plain"}

    @classmethod
    def image(cls, vid, ext):
        try:
            url = cls.imageMap[ext] + "{}/mqdefault.{}".format(vid, ext)
            data = req.fetch(url, 3600)
            return data, 200, {"Content-Type": "image/{}".format(ext), "Cache-Control": "public, max-age=604800"}
        except Exception as e:
            return str(e), 500, {"Content-Type": "text/plain"}

    @classmethod
    def videos(cls, args, params):
        url = cls.api.format("videos")
        return cls.json(url, args, params)

    @classmethod
    def search(cls, args, params):
        url = cls.api.format("search")
        return cls.json(url, args, params)

    @classmethod
    def channels(cls, args, params):
        url = cls.api.format("channels")
        return cls.json(url, args, params)

    @classmethod
    def playlists(cls, args, params):
        url = cls.api.format("playlists")
        return cls.json(url, args, params)

    @classmethod
    def playlistItems(cls, args, params):
        url = cls.api.format("playlistItems")
        return cls.json(url, args, params)

    @classmethod
    def categories(cls, args, params):
        url = cls.api.format("categories")
        return cls.json(url, args, params)
