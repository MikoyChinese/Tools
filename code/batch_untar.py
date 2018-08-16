import subprocess
import os

'''
eg: 
	root = /media/commaai-03/Data/tmp/
	dst = /media/commaai-03/Data/test/
	***Remember add '/' at end or you will get the error 'No such file or directory.'***
	-root is the path where your tars files saved.
	-dst is the path where you untar files save.
'''
root= '/media/commaai-03/Data/ori_data_sec/'
dst = '/media/commaai-03/Data/data_sec/'

for a, b, c in os.walk(top=root):
	for i in range(len(c)):
		dstPath = dst + c[i].split('.')[0]
		if not os.path.exists(dstPath):
			os.makedirs(dstPath)
		cmd = 'tar -xf %s --strip-components 3 -C %s' %(a+c[i], dstPath)
		subprocess.call(cmd, shell=True)
		#shell need true, nor you will get the error.
		print('-%s is untaring.' %(a+c[i]))
	print('>>> Finish!!!')
