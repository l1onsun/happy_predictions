from dataclasses import dataclass, field
from typing import Generic, Hashable, Optional, TypeVar

Key = TypeVar("Key", bound=Hashable)
Value = TypeVar("Value")


@dataclass
class LruCacheItem(Generic[Key, Value]):
    key: Key
    value: Value
    right: Optional["LruCacheItem"] = None
    left: Optional["LruCacheItem"] = None

    def remove_from_chain(self):
        if self.left:
            self.left.right = self.right
        if self.right:
            self.right.left = self.left


@dataclass
class LruCacheDict(Generic[Key, Value]):
    max_size: int
    _cached: dict[Key, LruCacheItem[Key, Value]] = field(
        default_factory=dict, init=False
    )
    far_left: Optional[LruCacheItem[Key, Value]] = field(default=None, init=False)
    far_right: Optional[LruCacheItem[Key, Value]] = field(default=None, init=False)

    def get(self, key: Key) -> Optional[Value]:
        if key not in self._cached:
            return None
        item = self._cached[key]
        item.remove_from_chain()
        return item.value

    def put(self, key: Key, value: Value) -> Value:
        if key in self._cached:
            self._cached[key].value = value
            return value
        self._cached[key] = new_item = LruCacheItem(key, value)
        self._append_left(new_item)
        if len(self._cached) > self.max_size:
            self._delete_far_right()
        return value

    def _append_left(self, item: LruCacheItem):
        self.far_left, item.right = item, self.far_left
        if not self.far_right:
            self.far_right = item

    def _delete_far_right(self):
        item_to_delete = self.far_right
        if not item_to_delete:
            return
        self.far_right = item_to_delete.left
        if self.far_right:
            self.far_right.right = None
        del self._cached[item_to_delete.key]
