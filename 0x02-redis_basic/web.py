#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and cache it"""
    r.set(f"cached:{url}", count)
    _response = requests.get(url)
    r.inr(f"count:{url}")
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return _response.text


if __name__ == "__main__":
    get_page('http://slowly.robertomurray.co.uk')
