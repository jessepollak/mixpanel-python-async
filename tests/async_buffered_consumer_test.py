#!/usr/bin/env python
import base64
import contextlib
import json
import unittest
import urlparse
import thread
import datetime
import time
import sys
import mixpanel

sys.path.append('../')

try:
    from mock import Mock, patch, DEFAULT
except ImportError:
    raise Exception(
        """
        mixpanel-python-async requires the mock package to run the test suite. 
        Please run: 

            $ pip install mock
        """)

from mixpanel_async import AsyncBufferedConsumer

class AsyncBufferedConsumerTestCase(unittest.TestCase):
    MAX_SIZE = 5
    ENDPOINT = 'people'
    JSON = json.dumps(dict(test=True))

    def setUp(self):
        self.consumer = AsyncBufferedConsumer(
            max_size=self.MAX_SIZE, 
            flush_first=False
        )

    @patch.object(mixpanel.BufferedConsumer, '_flush_endpoint')
    def test_sync_flush_endpoint_calls_buffered_consumer_flush_endpoint(self, _flush_endpoint):
        self.send_event()

        self.assertFalse(_flush_endpoint.called)

        self.consumer._sync_flush(endpoint=self.ENDPOINT)

        _flush_endpoint.assert_called_once_with(self.ENDPOINT)


    @patch.object(mixpanel.BufferedConsumer, '_flush_endpoint')
    def test_sync_flush_calls_buffered_consumer_flush_endpoint(self, flush_endpoint):
        self.send_event()

        self.assertFalse(flush_endpoint.called)

        self.consumer._sync_flush()

        flush_endpoint.assert_called_with(self.ENDPOINT)


    @patch.object(AsyncBufferedConsumer, '_sync_flush')    
    def test_flush_gets_called_in_different_thread_if_async(self, sync_flush):
        main_thread_id = thread.get_ident()
        flush_thread_id = None

        def side_effect(endpoint=None):
            self.assertNotEqual(main_thread_id, thread.get_ident())
            return DEFAULT

        sync_flush.side_effect = side_effect

        self.send_max_events()
        self.wait_for_threads()

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_flush_gets_called_in_same_thread_if_not_async(self, sync_flush):
        main_thread_id = thread.get_ident()
        flush_thread_id = None

        def side_effect(endpoint=None):
            self.assertEqual(main_thread_id, thread.get_ident())
            return DEFAULT

        sync_flush.side_effect = side_effect

        self.send_event()
        self.consumer.flush(async=False)

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_flushes_after_first_event_if_first_flush_true(self, sync_flush):
        self.consumer = AsyncBufferedConsumer(max_size=self.MAX_SIZE)

        self.send_event()
        self.wait_for_threads()

        sync_flush.assert_called_once_with()

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_does_not_flush_after_first_event_if_first_flush_false(self, sync_flush):
        self.send_event()
        self.wait_for_threads()

        self.assertFalse(sync_flush.called)

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_endpoints_get_flushed_when_they_hit_max_size(self, sync_flush):
        self.send_event("events")
        self.send_max_events()
        self.wait_for_threads()

        sync_flush.assert_called_once_with(endpoint=self.ENDPOINT)

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_all_events_get_flushed_after_flush_after(self, sync_flush):
        self.consumer.flush_after = datetime.timedelta(0, .5)

        self.send_event()
        self.assertFalse(sync_flush.called)

        time.sleep(.6)
        self.send_event()

        self.wait_for_threads()

        sync_flush.assert_called_once_with()

    @patch.object(AsyncBufferedConsumer, '_sync_flush')
    def test_endpoint_events_get_flushed_instantly_with_max_size_1(self, sync_flush):
        self.consumer = AsyncBufferedConsumer(max_size=1, flush_first=False)

        self.send_event()

        self.wait_for_threads()

        sync_flush.assert_called_once_with(endpoint=self.ENDPOINT)

    def test_does_not_drop_events(self):
        self.consumer = AsyncBufferedConsumer(flush_first=True)
        send_patch = patch.object(self.consumer._consumer, 'send').start()

        self.send_event()
        self.send_event()

        self.wait_for_threads()

        send_patch.assert_called_once_with(self.ENDPOINT, '[{"test": true}]')
        self.assertEqual(self.consumer._async_buffers[self.ENDPOINT], [self.JSON])

    def send_event(self, endpoint=None):
        endpoint = endpoint or self.ENDPOINT
        self.consumer.send(endpoint, self.JSON)

    def send_max_events(self):
        for i in range(self.MAX_SIZE):
            self.send_event()

    def wait_for_threads(self):
        if not self.consumer._flush_thread_is_free():
            self.consumer.flushing_thread.join()


if __name__ == "__main__":
    unittest.main()
