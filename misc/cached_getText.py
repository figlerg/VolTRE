# misc/text_cache.py
from functools import cached_property, lru_cache


@lru_cache(maxsize=None)
def _get_text(node):
    return node.getText()

