[Home Page](http://github.com/vonzhou/Blog)       ` ` ` ` ` ` ` ` ` `[vonzhou@163.com](http://weibo.com/u/3212472250)

---
# 在Mac上安装Latex 
---
Tag:latex, tool
---

工欲善其事，必先利其器。之所以想学习LaTeX的原因是，学习有些数学的时候需要推导表述，LaTeX很方便，安装也花了几个小时，特此记录下基本步骤。


#### Hello LateX

1. 下载安装MacTex，2.6G左右，不难；
2. 然后写个hello world，找到应用程序下面的Tex,就是我们安装的东西，然后看里面的文档First，打开TexShop，操作一番，不难；
3. 运行排版可以看到最终的pdf，但是出现了问题说“/usr/texbin/pdflatex不存在....”，相应的执行程序显然安装了，只是路径不对需要连接过去；
4. 运行 sudo ln -s /Library/TeX/Distributions/.DefaultTeX/Contents/Programs/texbin   /usr/texbin,说Operation not permitted, 这是因为系统的保护机制，需要修改；
5. 重启，长按Command+r 进行保护模式，打开终端，运行csrutil disable ,然后重启，OK
6. 可以看到简单的文档显示为PDF了。


### 安装 Sublime插件

1. 安装Sublime，安装[package control](https://packagecontrol.io/installation#st2)
2. Command_+shift + P 打开package controll manager ,选择 install packages;
3. install LatexTools插件（直接安装latexing后，却无法正常显示中文，所以选择LaTeX Tools）
4. 安装Skim，这是上述插件会调用的pdf阅读器
5.测试：
```
 
%!TEX program = xelatex
\documentclass[UTF-8]{ctexart}
\begin{document}

你好，LaTeX？

\end{document}

```

6. Command + B就可以编译，skim显示最终的pdf；



