from typing import Any

JsonType = dict[str, Any]


def url_join(*urls: str):
    return "/".join([url.strip("/") for url in urls])
