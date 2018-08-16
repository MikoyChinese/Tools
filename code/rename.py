#coding: utf-8
import os
import shutil

'''
对文件进行重命名
'''

for a, b, c in os.walk(top='/media/commaai-03/Data/1501270'):
	n = len(c)
	for i in range(n):
		name = '151270'
		new_name =  a + '/' + name+'_' +c[i].split('_')[1] + '_' + c[i].split('_')[2] + '_' + c[i].split('_')[3] + '_' + c[i].split('_')[4] + '_' + c[i].split('_')[5]
		#print new_name
		os.rename(a + '/' + c[i], new_name)
		
