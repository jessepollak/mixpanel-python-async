mixpanel-python-async
===============
This library allows for using the Mixpanel python client in an asynchronous way. Using the AsyncBufferedConsumer, events sent to the Mixpanel API will be batched and then flushed in a thread without blocking the main thread. This is extremely useful in a request/response scenario where response time is important.

This library was originally created for use at [Clef](https://getclef.com) and is in production use there.

Installation
------------
The library can be installed using pip:

    pip install mixpanel-py-async

Getting Started
---------------
Typical usage usually looks like this:

    #!/usr/bin/env python
    from mixpanel import Mixpanel
    from mixpanel_async import AsyncBufferedConsumer

    mp = Mixpanel(YOUR_TOKEN, consumer=AsyncBufferedConsumer())

    # tracks an event with certain properties
    mp.track('distinct_id', 'event name', {'color' : 'blue', 'size': 'large'})

    # sends an update to a user profile
    mp.people_set(USER_ID, {'$first_name' : 'Amy', 'favorite color': 'red'})

These events will be batched and then sent in a seperate, asynchronous thread.

### Configuration

For most users, the default configuration should work perfectly. For more specific needs, AsyncBufferedConsumer has a variety of configuration options, which you can use to manage how it batches and sends API requests.


* `flush_after (datetime.timedelta)` - *defaults to 10 seconds*  - the time period after which the AsyncBufferedConsumer will flush the events upon receiving a new event (no matter what the event queue size is)

* `flush_first (bool)` - *defaults to True* - whether the consumer should always flush the first event.

* `max_size (int)` - *defaults to 20* - how big a given event queue can get before it is flushed by the consumer

* `events_url (str)` - *defaults to standard Mixpanel API URL* - the Mixpanel API URL that track events will be sent to

* `people_url (str)` - *defaults to standard Mixpanel API URL* - the Mixpanel API URL that people events will be sent to

### Usage

Typically, after configuring the AsyncBufferedConsumer and passing it to the Mixpanel object, you will never have to use it again. That said, there are a few methods which can be useful.

* `flush()` - tells the AsyncBufferedConsumer to flush all of the events in its queues. If you call it with `async_=False` this flush will happen in the main thread (useful for ensuring all events are sent before a process ends)

```python
#!/usr/bin/env python
from mixpanel import Mixpanel
from mixpanel_async import AsyncBufferedConsumer

consumer = AsyncBufferedConsumer()
mp = Mixpanel(YOUR_TOKEN, consumer=consumer)

# tracks an event with certain properties
mp.track('distinct_id', 'event name', {'color' : 'blue', 'size': 'large'})

consumer.flush(async_=False)
# all events are flushed and process ends
```

Bugs
----

If you find an issue, let us know in the issues section!

Contributing
------------

From the [Rubinius](http://rubini.us/) contribution page:

> Writing code and participating should be fun, not an exercise in
> perseverance. Stringent commit polices, for whatever their other
> qualities may bring, also mean longer turnaround times.

Submit a patch and once it's accepted, you'll get commit access to the
repository. Feel free to fork the repository and send a pull request,
once it's merged in you'll get added. If not, feel free to bug
[jessepollak](http://github.com/jessepollak) about it.

How To Contribute
-----------------

* Clone: `git@github.com:jessepollak/mixpanel-python-async.git`
* Create a topic branch: `git checkout -b awesome_feature`
* Commit away (and add unit tests for any code your write).
* Keep up to date: `git fetch && git rebase origin/master`.
* Run the tests: `python setup.py test`

Once you're ready:

* Fork the project on GitHub
* Add your repository as a remote: `git remote add your_remote your_repo`
* Push up your branch: `git push your_remote awesome_feature`
* Create a Pull Request for the topic branch, asking for review.

Once it's accepted:

* If you want access to the core repository feel free to ask! Then you
can change origin to point to the Read+Write URL:

```
git remote set-url origin git@github.com:jessepollak/mixpanel-python-async.git
```

Otherwise, you can continue to hack away in your own fork.

*thanks to [rubygems](https://github.com/rubygems/rubygems.org) for inspiration of our guidelines*

Additional Information
----------------------

[Mixpanel python docs](https://www.mixpanel.com/help/reference/python)
[Mixpanel client libary](http://mixpanel.github.io/mixpanel-python/)

