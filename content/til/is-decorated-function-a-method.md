---
Title: Detecting if a decorated function would be a bound method if called
Date: 2025-03-30
Category: TIL
Description: TIL how to dynamically detect if a decorated function would be a a bound method when called.
Summary: TIL how to dynamically detect if a decorated function would be a a bound method when called.
Tags: Python, Programming
---

I was recently writing a caching decorator for a recent [project](https://github.com/brouberol/phable), that would allow me to cache the result of a given function or method into a cache singleton, which content is then serialized to disk when the CLI exits.

The decorator simply works like this:

```python
class PhabricatorClient:
    ...
    @cached
    def show_user(self, user_phid: str) -> dict:
        ...
```

`cached` builds a caching key formatted by separating all `args` as well as all `<key>=<value>` `kwargs` by `__`. In the previous example, if `PhabricatorClient.show_user(user_phid='12345')` would simply generate a cache key of `phid_id=12345`.

However, there's a catch. The first argument taken by this method is `self`: the `PhabricatorClient` instance, which should not be included in the cache key. I could have simply always omitted the first argument, but that would assume that this `cached` decorator would _always_ be wrapping methods. I wanted to be able to detect if the decorator was wrapping a method at runtime.

I initially tried [`inspect.ismethod`](https://docs.python.org/3/library/inspect.html#inspect.ismethod), which, to my surprise, returned `False`. After thinking about it, I realized that `inspect.ismethod` only returns `True` for _bound_ methods, which I is not true in the context of the decorator, as it is decorating a `PhabricatorClient.show_user`, not `PhabricatorClient().show_user`:

```python
>>> PhabricatorClient.show_user
<function PhabricatorClient.show_user at 0x102295040>
>>> inspect.ismethod(PhabricatorClient.show_user)
False
>>> PhabricatorClient().show_user
<bound method PhabricatorClient.show_user of <phable_cli.phabricator.PhabricatorClient object at 0x100f10b80>>
>>> inspect.ismethod(PhabricatorClient().show_user)
True
```

What I needed was a way to inspect the signature of the decorated function, to determine whether its first argument was named `self`. And this is what [`inspect.signature`](https://docs.python.org/3/library/inspect.html#inspect.signature) can be used for.

```python
>>> from phable_cli.phabricator import PhabricatorClient
>>> import inspect
>>> inspect.signature(PhabricatorClient.show_user).parameters
mappingproxy(OrderedDict([('self', <Parameter "self">), ('phid', <Parameter "phid: str">)]))
>>> list(inspect.signature(PhabricatorClient.show_user).parameters)[0]
'self'
```

In the end, my `cached` decorator read like [this](https://github.com/brouberol/phable/blob/18b53ea29e927472146c8a7e82e6c2f9c33801e3/phable_cli/cache.py#L46-L89):

```python
def cached(*cached_args, **cached_kwargs):
    """Cache the return value of the decorated function in memory.

    If a `ttl` keyword argment (of type typedelta) is passed to the decorator,
    the cached value will only be valid for the provided duration.

    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Check if the decorated function takes a `self` parameter, which is then omitted
            # from the cache key, as we just care about the other arguments, not the class itself.
            if list(inspect.signature(f).parameters)[0] == "self":
                cache_args = args[1:]
            else:
                cache_args = args
            cache_key = "__".join(map(str, cache_args))
            cache_key += "__".join([f"{k}={v}" for k, v in kwargs.items()])
            section = f.__name__
            if section not in cache:
                cache[section] = {}
            if cache_hit := cache[section].get(cache_key):
                if (
                    cache_hit["valid_until"] is None
                    or cache_hit["valid_until"] > time.time()
                ):
                    return cache_hit["data"]
            data = f(*args, **kwargs)
            cache[section][cache_key] = {
                "data": data,
                "valid_until": (
                    (datetime.now() + cached_kwargs["ttl"]).timestamp()
                    if cached_kwargs.get("ttl")
                    else None
                ),
            }
            return data

        return wrapper
    # This allows the decorator to be used without argument (`@cached`)
    # or with some (`@cached(ttl=timedelta(days=1))`)
    if cached_args and callable(cached_args[0]):
        return decorator(cached_args[0])
    return decorator
```