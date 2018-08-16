import subprocess
import numpy as np
import os
import tarfile


# dir_txt是记录了需要打包的目录的绝对路径，每一行为需要打包的root_dir。
dir_txt = '/home/commaai-03/no_dirs01.txt'


# Call command like terminal
def sub_call(cmd):
    print('-->>>', cmd)
    # cmd = cmd.split(' ')
    result = subprocess.call(cmd)
    print('Exit code: ', result)


# 根据目录打包
def tar_root(root, dstPath):
    rootDir_lst = os.listdir(root)
    i = 0
    for dirName in rootDir_lst:
        srcPath = os.path.join(root, dirName)
        if os.path.isdir(srcPath):
            dstName = dstPath + str(dirName) + '.tar'
            tar_dir(srcPath, dstName)
            i += 1
    print(root, '全部打包完毕，一共打包%s 个CVID！' % i)


# 打包方法
def tar_dir(srcPath, dstName):
    with tarfile.open(dstName, 'w') as tar:
        tar.add(srcPath, arcname=os.path.basename(srcPath))
        print(dstName + '已经打包完毕!')


def div_dstPath(file, dstPath_lst):
    for dstPath in dstPath_lst:
        file_lst = os.listdir(dstPath)
        if file not in file_lst:
            dstPath = dstPath
            print('>>>>>>>>>This file path is %s.' %dstPath)
            break
    return dstPath

# 根据需要打包对象的绝对地址进行读取打包。
def tar_dirPath(dirs, dstPath_lst):
    i = 0
    for each in dirs:
        fileName = each.split('/')[-1] + '.tar'
        dstPath = div_dstPath(fileName, dstPath_lst)
        dstName = dstPath + fileName
        tar_dir(each, dstName)
        i += 1
    print('>>>>>>All(%d) folder have tared FINISHED.!!!<<<<<<' % i)


if __name__ == '__main__':
    dirs  = np.loadtxt(dir_txt, dtype=str)
    dstPath_lst = ['/media/commaai-03/Free/tmp/',
                   '/media/commaai-03/Free/tmp2/',
                   '/media/commaai-03/Free/tmp3/']
    tar_dirPath(dirs, dstPath_lst)