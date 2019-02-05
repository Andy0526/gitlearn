# -*- coding: utf-8 -*-

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

APPID = 1400073392
APPKEY = 'fa14b1cde3741f1b8bfa6292f751a93f'
# ssender = SmsSingleSender(APPID, APPKEY)
# try:
#     result = ssender.send(0, 86, 17600718026, "你正在注册陪我，验证码是111111，请在2分钟内完成验证。请勿将验证码告知他人，验证码泄漏可能导致账号被盗。")
#     print result
# except HTTPError as e:
#     print(e)
# except Exception as e:
#     print(e)

from qcloudsms_py import SmsVoicePromptSender
from qcloudsms_py.httpclient import HTTPError

vvcsender = SmsVoicePromptSender(APPID, APPKEY)
try:
    result = vvcsender.send(86, 17611412502, 2, "你正在使用陪我，验证码是123453，请在2分钟内完成验证。", 2)
    print(result)
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)
