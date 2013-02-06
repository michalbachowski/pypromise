PyPromise
=========

PyPromise i open source (New BSD License)) Python Promise implementation. 
Simplifies working with asynchronous code and unifies way asynchronous and synchronous code is called.

Manual installation
-------------------

Download the latest release from http://github.com/michalbachowski/pypromise

    tar xvzf pypromise-$VERSION.tar.gz
    cd pypromise-$VERSION
    python setup.py build
    sudo python setup.py install

The PyPromise source code is hosted on GitHub: http://github.com/michalbachowski/pypromise

It is also possible to simply add the PyPromise directory to your PYTHONPATH instead of building with setup.py,
since it uses only standard parts of Python library.

Usage
-----

### Basic example:

1. Instantinate promise.Deferred 
2. attach as many callbacks (both done or fail) as you want
3. wait for resolution/rejection (eg. from asynchronous action)

```python
import promise
# chaining madness in action :D
defer = promise.Deferred().done(my_callback).fail(on_error_cb).then(on_success, other_on_error_cb)
some_async_action(callback=defer.resolve)
```

When "some_async_action" will finish and return result to "defer.resolve" all "done" callbacks ("my_callback" and "on_success") will be trigerred. In this example error callbacks **will not** be called - in order to do that one should call "defer.reject" manually.

### Deferred input arguments

Deferred object can accept both callable and non-callable input argument. When callable is given it will be called with "deferred" keyword argument pointing to Deferred`s "self". When non-callable is given it is considered as resolution for Deferred instance.

```python
promise.Deferred(123).resolved # True
promise.Deferred(lambda deferred: 1).resolved # False
```

### Promise

Promise is just proxy that makes Deferreds read-only.

```python
import promise
promise.Deferred().promise().resolve() # RuntimeException
```

### "when" helper

Using "promise.when" simplifies managing multiple asynchronous actions. This function returns Promise instance.

```python
import promise

def success(resp_action1, resp_action2):
    pass

def failure(*args, **kwargs):
    pass

promise.when(Deferred(async_action1), Deferred(async_action2)).then(success, failure)
```

"success" callback will receive response from both action in one call (as positional arguments passed in the same order as Deferred objects to 'when' helper) while "failure" callback will receive only one failure data (will be called just once).
One can pass either Deferred instance and await resolution or non-Deferred object which will be considered as immediate resolution for itself. You can mix Deferred and non-Deferred objects in one call.

```python
import promise
promise.when(Deferred(async_action), 'foo').resolved # False
promise.when('foo', 123).resolved # True
```
