# -*- coding: utf-8 -*-

# import gevent
#
# def foo():
#     print('Running in foo.')
#     gevent.sleep(0)
#     print('Explicit context to foo again.')
#
#
# def bar():
#     print('Explicit context to bar')
#     gevent.sleep(0)
#     print('Implicit context switch back to bar')
#
#
# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar)
# ])

# import time
# import gevent
# from gevent import select
#
# start = time.time()
# tic = lambda: 'at %1.f seconds' % (time.time() - start)
#
#
# def gr1():
#     print('Started Polling in gr1: %s' % tic())
#     select.select([], [], [], 2)
#     print('Ended Polling in gr1: %s' % tic())
#
#
# def gr2():
#     print('Started Polling in gr2: %s' % tic())
#     select.select([], [], [], 2)
#     print('Ended Polling in gr2: %s' % tic())
#
#
# def gr3():
#     print("Hey lets do some stuff while the greenlets poll, %s" % tic())
#     gevent.sleep(1)
#
#
# gevent.joinall([
#     gevent.spawn(gr1),
#     gevent.spawn(gr2),
#     gevent.spawn(gr3),
# ])

# import gevent
# import random
#
#
# def task(pid):
#     """
#     Some non-deterministic task
#     """
#     gevent.sleep(random.randint(0, 2) * 0.001)
#     print('Task %s done' % pid)
#
#
# def synchronous():
#     for i in range(1, 10):
#         task(i)
#
#
# def asynchronous():
#     threads = [gevent.spawn(task, i) for i in range(10)]
#     gevent.joinall(threads)
#
#
# print('Synchronous:')
# synchronous()
# print('Asynchronous:')
# asynchronous()


# import gevent
# from gevent import Greenlet
#
#
# def foo(message, n):
#     gevent.sleep(n)
#     print(message)
#
#
# thread1 = Greenlet.spawn(foo, "Hello", 1)
# thread2 = Greenlet.spawn(foo, 'I live', 2)
# gevent.joinall([thread1, thread2])
#

# import gevent
# from gevent import Greenlet
#
#
# class MyGreenlet(Greenlet):
#     def __init__(self, message, delay):
#         Greenlet.__init__(self)
#         self.message = message
#         self.delay = delay
#
#     def _run(self):
#         print(self.message)
#         gevent.sleep(self.delay)
#
#
# g = MyGreenlet('Hi there', 1)
# print(g.started)
# g.start()
# print(g.started)
# g.join()
# print(g.successful())


import gevent
from gevent import Timeout


def wait():
    gevent.sleep(2)


timer = Timeout(1).start()
thread1 = gevent.spawn(wait)
try:
    thread1.join(timeout=timer)
except Timeout:
    print('Thread 1 timed out')

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait)
try:
    thread2.get(timeout=timer)
except Timeout:
    print('Thread 2 timed out')

try:
    gevent.with_timeout(1, wait)
except Timeout:
    print('Thread 3 timed out')
