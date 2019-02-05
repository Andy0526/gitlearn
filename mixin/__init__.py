# # -*- coding: utf-8 -*-
# from datetime import datetime, date
#
# SIGNUP_SETTING = [(0, 24, 5), (24, 48, 4), (48, 72, 3), (72, 120, 2), (120, 168, 1), (168, None, 0)]
# format_str = '%Y-%m-%d %H:%M:%S'
#
#
# def str_to_dt(dt_str):
#     if not dt_str:
#         return
#     if isinstance(dt_str, datetime):
#         return dt_str
#     elif isinstance(dt_str, date):
#         return datetime(dt_str.year, dt_str.month, dt_str.day)
#     try:
#         return datetime.strptime(dt_str, format_str)
#     except:
#         pass
#
#
# def find_score(setting, value):
#     for each_setting in setting:
#         if each_setting[0] is not None and each_setting[0] > value:
#             pass
#         elif each_setting[1] is not None and each_setting[1] < value:
#             pass
#         else:
#             return each_setting[2]
#     return 0
#
#
# if __name__ == '__main__':
#     signup_time = '2016-06-14 14:00:59'
#     hours = (datetime.now() - str_to_dt(signup_time)).seconds
#     print(hours)
#     print(find_score(SIGNUP_SETTING, hours))


# class Signleton(object):
#     def __new__(cls, *args, **kwargs):
#         if hasattr(cls, '_instance'):
#             return cls._instance
#         cls._instance = super(Signleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# class MyClass(Signleton):
#     a = 1
#
#
# one = MyClass()
# two = MyClass


# class Signleton(object):
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '_instance'):
#             cls._instance = super(Signleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# class MyClass(Signleton):
#     a = 1
#
#
# one = MyClass()
# two = MyClass()
# one.a = 3
# print(one.a, two.a)
# print(id(one), id(two))
#
#
# class Brog(object):
#     _state = {}
#
#     def __new__(cls, *args, **kwargs):
#         obj = super(Brog, cls).__new__(cls, *args, **kwargs)
#         obj.__dict__ = cls._state
#         return obj


# class Signleton(type):
#
#     def __init__(cls, name, bases, attrs):
#         super(Signleton, cls).__init__(name, bases, attrs)
#         cls._instances = None
#
#     def __call__(cls, *args, **kwargs):
#         if not cls._instances:
#             cls._instances = super(Signleton, cls).__call__(*args, **kwargs)
#         return cls._instances
#
#
# class MyClass(object):
#     __metaclass__ = Signleton

class Singleton2(type):
    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        return cls._instance


class MyClass3(object):
    __metaclass__ = Singleton2


one = MyClass3()
two = MyClass3()

two.a = 3
# print(one.a)
# 3
print(id(one))
# 31495472
print(id(two))
# 31495472
print(one == two)
# True
print(one is two)
# True

