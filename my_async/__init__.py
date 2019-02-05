# -*- coding: utf-8 -*-

import time
import asyncio

now = lambda: time.time()


# async def do_some_work(x):
#     print('Waiting: ', x)
#
#
# start = now()
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(do_some_work(2))
# print('Time: ', now() - start)

async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


start = now()
loop = asyncio.get_event_loop()
