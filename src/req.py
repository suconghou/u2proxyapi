import time
import urllib2


class memcache:
    def __init__(self):
        self.cache = dict()

    def set(self, key, value, ttl=86400):
        self.cache[key] = [value, time.time()+ttl]

    def get(self, key):
        v = self.cache.get(key)
        if not v:
            return None
        [value, expire] = v
        if expire > time.time():
            return value
        self.expire()
        return None

    def expire(self):
        t = time.time()
        for k, v in list(self.cache.items()):
            [value, expire] = v
            if expire < t:
                k in self.cache and self.cache.pop(k)


cache = memcache()


def fetch(url, ttl=86400):
    v = cache.get(url)
    if v:
        return v
    res = urllib2.urlopen(url, None, 20)
    code = res.getcode()
    if code == 200:
        data = res.read()
        if data:
            cache.set(url, data, ttl)
        return data
    raise IOError("HTTP Error {}".format(code))
