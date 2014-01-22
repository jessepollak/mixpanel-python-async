mixpanel-python-async
===============
This library allows for using the Mixpanel python client in an asynchronous way. Using the AsyncBufferedConsumer, events sent to the Mixpanel API will be batched and then flushed in a thread without blocking the main thread. This is extremely useful in a request/response scenario where response time is important.

Installation
------------
The library can be installed using pip:

    pip install mixpanel-py-async

Getting Started
---------------
Typical usage usually looks like this:

    #!/usr/bin/env python
    from mixpanel import Mixpanel
    from mixpanel_async import AsynBufferedConsumer

    mp = Mixpanel(YOUR_TOKEN, consumer=AsyncBufferedConsumer())

    # tracks an event with certain properties 
    mp.track('button clicked', {'color' : 'blue', 'size': 'large'})

    # sends an update to a user profile
    mp.people_set(USER_ID, {'$first_name' : 'Amy', 'favorite color': 'red'})

These events will be batched and then sent in a seperate, asynchronous thread.

Additional Information
----------------------

[Mixpanel python docs](https://www.mixpanel.com/help/reference/python)
[Mixpanel client libary](http://mixpanel.github.io/mixpanel-python/)

