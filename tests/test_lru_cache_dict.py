from happy_predictions.predictor.lru_cache import LruCacheDict


def test_lru_cache_dict_len_one():
    cache = LruCacheDict[str, int](max_size=1)
    assert cache.get("one") is None

    assert cache.put("one", 1) == 1
    assert cache.get("one") == 1
    assert cache.far_left == cache.far_right
    assert len(cache._cached) == 1

    assert cache.put("two", 2) == 2
    assert cache.get("one") is None
    assert cache.get("two") == 2
