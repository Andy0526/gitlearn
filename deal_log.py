#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import re
#
# FILE_IN = 'match_with_pool.txt'
# FILE_OUT = 'dealed.log'
#
#
# def deal_log():
#     with open(FILE_IN, 'r') as f_in:
#         with open(FILE_OUT, 'a') as f_out:
#             for line in f_in.readlines():
#                 params = re.findall('\d{6,11}:', line)
#                 if params:
#                     uids = ','.join([param.split(':')[0] for param in params])
#                     splits = re.split('\d{6,11}:', line)
#                     splits_2 = splits[-1]
#                     f_out.write(splits[0] + uids + '}' + re.split('},', splits_2)[-1])
#                 else:
#                     if ':{}, wild_male_pool' in line:
#                         f_out.write(line)
#
#
# if __name__ == '__main__':
#     deal_log()

from datetime import datetime
import matplotlib.pyplot as plt  # 引入绘图库


def draw_plot():
    time_lst = []
    pool_lst = []
    pool_1_lst = []
    pool_2_lst = []
    with open('data.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            time_str, pool, pool1, pool2 = line.split('\t')
            time_lst.append(datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S').date())
            pool_lst.append(pool)
            pool_1_lst.append(pool1)
            pool_2_lst.append(pool2)
    plt.plot(time_lst, pool_lst, label='pool')
    plt.xlabel('时间')
    plt.ylabel('人数')
    plt.title('男性优质')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    draw_plot()

# if __name__ == '__main__':
#
#     # 打开文本文件 读取数据
#     with open("data.txt", 'r', encoding='utf-8') as f:
#         data_lines = f.readlines()
#
#     l_time = []
#     l_visit = []
#
#     num = len(data_lines)
#
#     # ################
#     #     整理数据
#     # ################
#     for i in range(1, num):
#         line = data_lines[i].strip()  # 从第1行开始[0行开始计数]
#         if len(line) < 2:
#             continue  # 这行明显不是有效信息
#         data = line.split(' ')
#         time = data[0]
#         visit = int(data[6])
#         l_time.append(time)
#         l_visit.append(visit)
#
#     # ################
#     #       画图
#     # ################
#     # X坐标，将str类型的数据转换为datetime.date类型的数据，作为x坐标
#     xs = [datetime.strptime(d, '%Y/%m/%d').date() for d in l_time]
#
#     plt.figure(1)
#     plt.subplot(1, 3, 1)
#     plt.title('Visit Number')
#     plt.plot(xs, l_visit, 'o-')
#     plt.xlabel('Time')
#     plt.ylabel('Visit Number')
#
#     # 只画最后一个元素点 - 数据点在文字的↘右下，文字在↖左上
#     plt.text(xs[-1], l_visit[-1], l_visit[-1], ha='right', va='bottom', fontsize=10)
#
#     plt.gcf().autofmt_xdate()  # 自动旋转日期标记
#
#     # show
#     plt.show()
