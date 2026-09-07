import time

CACHE = {}

CACHE_TTL_SECONDS = 300


def get_cached(key: str):
    item = CACHE.get(key)

    if not item:
        return None

    if time.time() - item["timestamp"] > CACHE_TTL_SECONDS:
        del CACHE[key]
        return None

    return item["value"]


def set_cached(key: str, value):
    CACHE[key] = {
        "timestamp": time.time(),
        "value": value
    }