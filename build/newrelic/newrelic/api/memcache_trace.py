from __future__ import with_statement

import sys
import types
import inspect
import time

import newrelic.core.memcache_node

import newrelic.api.transaction
import newrelic.api.time_trace
import newrelic.api.object_wrapper

class MemcacheTrace(newrelic.api.time_trace.TimeTrace):

    node = newrelic.core.memcache_node.MemcacheNode

    def __init__(self, transaction, command):
        super(MemcacheTrace, self).__init__(transaction)

        self.command = command

    def create_node(self):
        return self.node(command=self.command, children=self.children,
                start_time=self.start_time, end_time=self.end_time,
                duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True

class MemcacheTraceWrapper(object):

    def __init__(self, wrapped, command):
        if type(wrapped) == types.TupleType:
            (instance, wrapped) = wrapped
        else:
            instance = None

        newrelic.api.object_wrapper.update_wrapper(self, wrapped)

        self._nr_instance = instance
        self._nr_next_object = wrapped

        if not hasattr(self, '_nr_last_object'):
            self._nr_last_object = wrapped

        self._nr_command = command

    def __get__(self, instance, klass):
        if instance is None:
            return self
        descriptor = self._nr_next_object.__get__(instance, klass)
        return self.__class__((instance, descriptor), self._nr_command)

    def __call__(self, *args, **kwargs):
        transaction = newrelic.api.transaction.transaction()
        if not transaction:
            return self._nr_next_object(*args, **kwargs)

        if not isinstance(self._nr_command, basestring):
            if self._nr_instance and inspect.ismethod(self._nr_next_object):
                command = self._nr_command(self._nr_instance, *args,
                                           **kwargs)
            else:
                command = self._nr_command(*args, **kwargs)
        else:
            command = self._nr_command

        with MemcacheTrace(transaction, command):
            return self._nr_next_object(*args, **kwargs)

def memcache_trace(command):
    def decorator(wrapped):
        return MemcacheTraceWrapper(wrapped, command)
    return decorator

def wrap_memcache_trace(module, object_path, command):
    newrelic.api.object_wrapper.wrap_object(module, object_path,
            MemcacheTraceWrapper, (command,))
