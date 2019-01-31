import platform
import subprocess

import codecs

# 根据平台不同使用marked命令不同
marked_cmd = "marked.cmd"
p = platform.platform()
if "Windows" not in p:
    marked_cmd = "marked"


# 处理写UTF-8到文件，需要这样
file = codecs.open("index.html","w", "utf-8") 
start = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta http-equiv="X-UA-Compatible" content="ie=edge" /><title>Document</title></head><body>""" 
end = """</body></html>"""

# 1.写头部
file.write(start)


# 2. 写内容， 使用marked把MD转化为html
myinput = open('README.md', "r")
process = subprocess.Popen([marked_cmd], stdin=myinput, stdout=subprocess.PIPE)
out, err = process.communicate()
file.write(out.decode('utf-8'))

# 3.写尾部
file.write(end)

file.close() 