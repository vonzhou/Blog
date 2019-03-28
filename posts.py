#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import os
from os import listdir
from os.path import isfile, join


print("update posts list in readme")

postsDir = "content/posts"


onlyfiles = [f for f in listdir(postsDir) if isfile(join(postsDir, f))]

postTitleAndDate = {}

# 博客标题占位符
TITLE = "title: "
# 博客日期占位符
DATE = "date: "
# 最终生成的posts列表
res = os.linesep

for f in onlyfiles:
    tmp = postsDir + "/" + f
    with open(tmp, "r", encoding="UTF-8") as f:
        content = f.readlines()
        title = ""
        date = ""
        entry = ""
        for line in content:
            if(line.startswith(TITLE)):
                title = line[line.index(TITLE) + len(TITLE):]
                title = title[1:len(title)-2]
                entry = entry + "[" + title + "](" + tmp + ")"
            if(line.startswith(DATE)):
                date = line[line.index(DATE) + len(DATE):]
                entry = entry + "  " + date
                break
        res = res + entry + os.linesep


# print(res)

readmeFile = "README.md"
originContent=""
with open(readmeFile, "r", encoding="UTF-8") as f:
    originContent = f.read()

# print(originContent)

left = originContent[:originContent.index("## 源文件")] + os.linesep
left = left + "## 源文件" + os.linesep

right = originContent[originContent.index("## 约定"):len(originContent)]

all = left + os.linesep + res + right

with open(readmeFile, "w", encoding="UTF-8") as f:
    f.write(all)

