#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This python file is a copy file tool by whatever you want.
# First methods is copying file by index. ['cvid'][index]!

import pandas as pd
import shutil


# 1.Copy file by index.
def copy_by_index(data):
    counts = len(data)
    file_paths = ['/media/commaai-03/Free/tmp/',
                  '/media/commaai-03/Free/tmp2/',
                  '/media/commaai-03/Free/tmp3/']
    for index in range(counts):
        first = data['first'][index]
        second = data['second'][index]
        if first != 0:
            file_path = file_paths[first-1]
            src = file_path + str(data['cvid'][index]) + '.tar'
            dst = '/media/commaai-03/Data/tmp/' + str(data['cvid'][index]) \
                  + '.tar'
            shutil.copy2(src, dst)
        if second != 0:
            file_path = file_paths[second-1]
            src = file_path + str(data['cvid'][index]) + '.tar'
            dst = '/media/commaai-03/Data/tmp2/' + str(data['cvid'][index]) \
                  + '.tar'
            shutil.copy2(src, dst)
        print('Cvid:%-10s First:%-8d Second:%-8d' % (data['cvid'][index], first,
                                                     second))
    print('================================Finish'
          '=================================')


# Read data by pandas <pd.read_excel(path)>.
def read_pd_excel(path, header=0):
    data = pd.read_excel(path, header)
    return data


if __name__ == '__main__':
    data_path = '/home/commaai-03/Documents/cvid数据处理20180807.xlsx'
    data = read_pd_excel(data_path)
    print('=================================Start'
          '=================================')
    # Starting copying.
    copy_by_index(data)
