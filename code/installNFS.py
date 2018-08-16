#This python file can install NFS server and client automatically.
# -*- coding: utf-8 -*-
import subprocess

#Call command like terminal
def sub_call(cmd):
    print('$', cmd)
    cmd = cmd.split(' ')
    result = subprocess.call(cmd)
    print('Exit code: ', result)
def configure():
    share_folder = input('Where you want to Share? Such like this: /home -->:')
    ip = input("*  所有可以ping同该主机的用户 /"
               "192.168.1.*  指定网段，在该网段中的用户可以挂载 /"
               "192.168.1.12 只有该用户能挂载")
    permission = input('ro : 只读'
                       'rw : 读写'
                       'no_root_squash: 不降低root用户的权限')
    with open('/etc/export', 'a+') as f:
        f.write('\n', )
        f.write('%s %s(insecure,%s,sync,fsid=0,no_roo_squash)' % (share_folder, ip, permission))
    sub_call('sudo service nfs-kernel-server restart')

if __name__ == "__main__":
    try:
        sub_call('sudo apt-get install nfs-kernel-server -y')
        configure()
    except PermissionError:
        PermissionError.args

