# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import logging
import random
import time
import traceback
import zlib

import requests
from ecdsa import SigningKey, util


def base64_encode_url(data):
    base64_data = base64.b64encode(data)
    base64_data = base64_data.replace('+', '*')
    base64_data = base64_data.replace('/', '-')
    base64_data = base64_data.replace('=', '_')
    return base64_data


def base64_decode_url(base64_data):
    base64_data = base64_data.replace('*', '+')
    base64_data = base64_data.replace('-', '/')
    base64_data = base64_data.replace('_', '=')
    raw_data = base64.b64decode(base64_data)
    return raw_data


class QCloudIM(object):
    APPID3RD = ''
    VERSION = 20161204
    EXPIRE = 3600 * 24 * 35

    ACCTYPE = 10694
    SDKAPPID = 1400025131
    PRI_KEY = """
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEICOmyaCZyFK3mIcnOQYcrCB+7saNGsg3YFVmWycVicj0oAcGBSuBBAAK
oUQDQgAEvVCyTtER/GNiNe0uwevOLq6gG6Gkp0/lGVyJXfcozdf69NIY06abdVFX
F+cu2HSSrpYbc6gxsq7JQnzjt40F5Q==
-----END EC PRIVATE KEY-----
"""

    #     if ENV_TEST:
    #         ACCTYPE = 9534
    #         SDKAPPID = 1400021717
    #         PRI_KEY = """
    # -----BEGIN EC PRIVATE KEY-----
    # MHQCAQEEIK23vu/ajGCsfAs2Vz3WTV2WphwnE477VUIZZaxqCfYIoAcGBSuBBAAK
    # oUQDQgAEHO8A+MLCstbVEiADuXXDBhGU8/h1T3Tf4k2vK1J05J9TebnCE/00XQpa
    # YEjECnWZdTTkgPEnzx6BFRF857YLeg==
    # -----END EC PRIVATE KEY-----
    # """

    @classmethod
    def get_sig(cls, identifier):
        sig = cls.generate_sig(identifier)
        return sig

    @classmethod
    def generate_sig(cls, identifier, expire=None):
        api = QCloudIM()

        sig_dct = api._gen_sig_dct(cls.SDKAPPID, cls.PRI_KEY, identifier, expire)

        json_str = json.dumps(sig_dct)
        sig_cmpressed = zlib.compress(json_str)
        base64_sig = base64_encode_url(sig_cmpressed)
        return base64_sig

    def _gen_sig_dct(self, sdkappid, pri_key, identifier, expire=None):
        sig_dct = self._create_dct(sdkappid, pri_key, identifier, expire)
        fix_str = self._encode_to_fix_str(sig_dct)

        pk_loaded = SigningKey.from_pem(pri_key)
        sig_field = pk_loaded.sign(fix_str, hashfunc=hashlib.sha256, sigencode=util.sigencode_der)
        sig_field_base64 = base64.b64encode(sig_field)
        sig_dct['TLS.sig'] = sig_field_base64

        return sig_dct

    def _create_dct(self, sdkappid, pri_key, identifier, expire=None):
        if not expire:
            expire = self.EXPIRE
        return {
            'TLS.account_type': str(self.ACCTYPE),
            'TLS.identifier': str(identifier),
            'TLS.appid_at_3rd': self.APPID3RD,
            'TLS.sdk_appid': str(sdkappid),
            'TLS.expire_after': str(expire),
            'TLS.version': str(self.VERSION),
            'TLS.time': str(int(time.time())),
        }

    def _encode_to_fix_str(self, sig_dct):
        fmt = 'TLS.appid_at_3rd:%s' + '\n' \
              + 'TLS.account_type:%s' + '\n' \
              + 'TLS.identifier:%s' + '\n' \
              + 'TLS.sdk_appid:%s' + '\n' \
              + 'TLS.time:%s' + '\n' \
              + 'TLS.expire_after:%s' + '\n'

        args = sig_dct['TLS.appid_at_3rd'], sig_dct['TLS.account_type'], sig_dct['TLS.identifier'], \
               sig_dct['TLS.sdk_appid'], sig_dct['TLS.time'], sig_dct['TLS.expire_after']

        return fmt % args


request_session = requests.Session()


def call_api(url, method, timeout=10.0, **kwargs):
    random_num = random.randrange(10000, 99999)
    t1 = time.time()

    identifier = 'admin'
    usersig = QCloudIM.get_sig(identifier)

    url2 = '%s?usersig=%s&identifier=%s&sdkappid=%s&random=%s&contenttype=json' % (
        url, usersig, identifier, QCloudIM.SDKAPPID, random_num)

    try:
        response = request_session.request(method, url2, verify=False, timeout=timeout, **kwargs)
        runtime = time.time() - t1
        logging.debug(
            'call_api url:%s args:%s response:%s time:%s' % (url, kwargs, response.text, runtime))
        result = json.loads(response.text)
        if result.get('ErrorCode', 0) != 0:
            err_info = 'qcloud_api_error url:%s args:%s response:%s' % (url, kwargs, response.text,)
            logging.error(err_info)
            # if int(result['ErrorCode']) in cls.INTERNAL_ERR_CODE:
            #     raise InternalError(err_info)
            # else:
            #     logging.error(err_info)
        return result
    except:
        runtime = time.time() - t1
        logging.error('call_api error, url:{}, {}'.format(url, traceback.format_exc()))
        return {'ErrorCode': 10000}


def update_user_info(uid, name=None, gender=None, image_url=None, state=None):
    values = []
    if name:
        values.append({'Tag': 'Tag_Profile_IM_Nick', 'Value': name})
    if image_url:
        values.append({'Tag': 'Tag_Profile_IM_Image', 'Value': image_url})
    if gender:
        value = 'Gender_Type_Male' if gender == 1 else 'Gender_Type_Female'
        values.append({'Tag': 'Tag_Profile_IM_Gender', 'Value': value})
    if state is not None:
        values.append({'Tag': 'Tag_Profile_Custom_State', 'Value': state})
    data = {
        'From_Account': str(uid),
        'ProfileItem': values
    }

    url = 'https://console.tim.qq.com/v4/profile/portrait_set'

    return call_api(url, 'POST', data=json.dumps(data))


def get_user_infos(uids):
    """
    获取账号信息
    :param uids:
    :return:
    """
    data = {
        'To_Account': [str(uid) for uid in uids],
        'TagList': [
            'Tag_Profile_Custom_State',
            'Tag_Profile_IM_Nick',
        ]
    }

    url = 'https://console.tim.qq.com/v4/profile/portrait_get'

    return call_api(url, 'POST', data=json.dumps(data))


if __name__ == '__main__':
    print update_user_info(21006, state=2)
    # print get_user_infos([21006, ])
