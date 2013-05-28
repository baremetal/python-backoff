Python Backoff Decorator
========================

This package implements exponential backoff as a decorator.  Backoff is
triggered by an exception and is reset when the call is successful.


Usage
-----

Apply exponential backoff to any function or method by simply adding the
decorator:

```python
import backoff
import requests

@backoff.Backoff()
def send_data(data):
    requests.post('https://example.com/data', data={'data': data})

try:
    send_data('foo')
except:
    # do something with data that wasn't posted
```

In the example above calls to `send_data()` will exponentially backoff when
POST is not successful.


Calls During Backoff Period
---------------------------

Any calls made during the backoff period will raise an `InBackoff` exception.


Setting Maximum Backoff
-----------------------

By default the maximum backoff is 1 hour.  The `max_backoff` argument can be
passed to change the default; the following will only backoff for 5 minutes:

```python
@backoff.Backoff(max_backoff=300)
def send_data(data):
    requests.post('https://example.com/data', data={'data': data})
```
