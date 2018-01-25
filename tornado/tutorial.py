# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan

# import tornado.ioloop
# import tornado.web
#
#
# class MainHandler(tornado.web.RequestHandler):
#
#     def get(self):
#         self.write('Hello, world')
#
#
# def make_app():
#     return tornado.web.Application([(r"/", MainHandler), ])
#
#
# if __name__ == "__main__":
#     app = make_app()
#     app.listen(9088)
#     tornado.ioloop.IOLoop.current().start()
#


# class IFakeSyncCall(object):
#     def __init__(self):
#         super(IFakeSyncCall, self).__init__()
#         self.generators = {}
#
#     @staticmethod
#     def FAKE_SYNCALL():
#         def fwrap(method):
#             def fakeSyncCall(instance, *args, **kwargs):
#                 print(instance, args, kwargs)
#                 instance.generators[method.__name__] = method(instance, *args, **kwargs)
#                 func, args = instance.generators[method.__name__].__next__()
#                 func(*args)
#
#             return fakeSyncCall
#
#         return fwrap
#
#     def onFakeSyncCall(self, identify, result):
#         try:
#             print('identify', identify)
#             func, args = self.generators[identify].send(result)
#             func(*args)
#         except StopIteration:
#             self.generators.pop(identify)
#
#
# import random
#
#
# class Player(object):
#     def __init__(self, entityId):
#         super(Player, self).__init__()
#         self.entityId = entityId
#
#     def onFubenEnd(self, mailBox):
#         score = random.randint(1, 10)
#         print("onFubenEnd player %d score %d" % (self.entityId, score))
#         mailBox.onFakeSyncCall('evalFubenScore', (self.entityId, score))
#
#
# class FubenStub(IFakeSyncCall):
#     def __init__(self, players):
#         super(FubenStub, self).__init__()
#         self.players = players
#
#     @IFakeSyncCall.FAKE_SYNCALL()
#     def evalFubenScore(self):
#         totalScore = 0
#         for player in self.players:
#             entityId, score = yield (player.onFubenEnd, (self,))
#             print("onEvalFubenScore player %d score %d" % (entityId, score))
#             totalScore += score
#
#         print('the totalScore is %d' % totalScore)
#
#
# if __name__ == '__main__':
#     players = [Player(i) for i in range(3)]
#
#     fs = FubenStub(players)
#     fs.evalFubenScore()

from werkzeug.utils import cached_property
