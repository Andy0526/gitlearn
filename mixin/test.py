# # -*- coding: utf-8 -*-
#
# class A:
#     def __init__(self):
#         self.n = 2
#
#     def add(self, m):
#         print('self is {0} @A.add'.format(self))
#         print(super())
#         self.n += m
#
#
# class B(A):
#     def __init__(self):
#         self.n = 3
#
#     def add(self, m):
#         print('self is {0} @B.add'.format(self))
#         print(super())
#         super(B, self).add(m)
#         self.n += 3
#
#
# class C(A):
#     def __init__(self):
#         self.n = 4
#
#     def add(self, m):
#         print('self is {0} @C.add'.format(self))
#         print(super())
#         super().add(m)
#         self.n += 4
#
#
# class D(B, C):
#     def __init__(self):
#         self.n = 5
#
#     def add(self, m):
#         print('self is {0} @D.add'.format(self))
#         print(super())
#         super().add(m)
#         self.n += 5
#
#
# d = D()
# d.add(2)
# print(d.n)


# def sub_sort(array, low, high):
#     key = array[low]
#     while low < high:
#         while low < high and array[high] >= key:
#             high -= 1
#         if low < high:
#             array[low] = array[high]
#         while low < high and array[low] < key:
#             low += 1
#         if low < high:
#             array[high] = array[low]
#         array[low] = key
#         return low
#
#
# def quick_sort_standard(array, low, high):
#     if low < high:
#         key_index = sub_sort(array, low, high)
#         quick_sort_standard(array, low, key_index)
#         quick_sort_standard(array, key_index + 1, high)
#
#
# if __name__ == '__main__':
#     array2 = [9, 3, 2, 1, 4, 6, 7, 0, 5]
#
#     print(array2)
#     quick_sort_standard(array2, 0, len(array2) - 1)
#     print(array2)
#
#

def sub_sort(array, low, high):
    key = array[low]
    while low < high:
        while low < high and array[high] >= key:
            high -= 1
        while low < high and array[high] < key:
            array[low] = array[high]
            low += 1
            array[high] = array[low]
    array[low] = key
    return low


def quick_sort_advanced(array, low, high):
    if low < high:
        key_index = sub_sort(array, low, high)
        quick_sort_advanced(array, low, key_index)
        quick_sort_advanced(array, key_index + 1, high)


if __name__ == '__main__':
    # array = [8,10,9,6,4,16,5,13,26,18,2,45,34,23,1,7,3]
    array1 = [7, 3, 5, 6, 2, 4, 1]

    print(array1)
    quick_sort_advanced(array1, 0, len(array1) - 1)
    print(array1)
