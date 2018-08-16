#_*_ coding:utf-8 _*_ 

import sys
import difflib

try:
	f1 = sys.argv[1]
	f2 = sys.argv[2]
	report = sys.argv[3]
except Exception as e:
	print('Error: ' + str(e))
	sys.exit()

def GetLines(file_name):
	return open(file_name).readlines()

txt_l1 = GetLines(f1)
txt_l2 = GetLines(f2)
diff = difflib.HtmlDiff()
fid = open(report, 'w')
fid.write(diff.make_file(txt_l1, txt_l2))
fid.close()
