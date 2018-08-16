import os
import tarfile
import argparse
'''
本脚本可以快速打包，以根目录内的文件为单位，进行分批打包！
root 需要打包的根目录，dstPath 打包后文件放置的路径
eg: --root=/media/commaai/data --dstPath=/media/commaai/dstPath  #注意，路径最后不要有'/'。，因为脚本已经添加了'/'进行处理了。
'''

parser = argparse.ArgumentParser(description='Process some parameter!')
parser.add_argument('--root', type=str, dest='root')
parser.add_argument('--dstPath', type=str, dest='dstPath')

args = parser.parse_args()

def tar_dir(srcPath, dstName):
	with tarfile.open(dstName, 'w') as tar:
		tar.add(srcPath, arcname=os.path.basename(srcPath))
		print(dstName + '已经打包完毕.')

if __name__ == '__main__':
	root = args.root
	dstPath = args.dstPath
	dir_lst = os.listdir(root)
	i = 0
	for dirName in dir_lst:
		srcPath = root + '/' + str(dirName)
		if os.path.isdir(srcPath):
			dstName = dstPath + '/' + str(dirName) + '.tar'
			tar_dir(srcPath, dstName)
			i += 1
	print('全部打包完毕, 一共打包' + str(i) + '个CVID！')
