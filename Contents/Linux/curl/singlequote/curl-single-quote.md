[主页](http://vonzhou.com)  | [读书](https://github.com/vonzhou/readings)  | [知乎](https://www.zhihu.com/people/vonzhou) | [GitHub](https://github.com/vonzhou)
---
# curl URL是否加单引号引发的问题
---



## 问题背景

后端实现了一个普通接口，浏览器中访问时OK的。

![](curl-single-quote-1.png)

但是bash中使用curl命令访问一直是400。

```bash
$ curl -v http://localhost:8181/app/test.do?k=x&b=yyy
```
![](curl-single-quote-2.png)

折腾了很久一直怀疑是自己服务的问题，殊不知是使用curl姿势的问题，URL中加上单引号就正常访问接口。

```bash
$ curl -v 'http://localhost:8181/app/test.do?k=x&b=yyy'
```

![](curl-single-quote-3.png)

其实遇到问题应该早早的debug，而不是盲目的猜测原因，如果debug就会发现传到后端的参数其实是被截取了的，所以参数不完整，出现400。

![](curl-single-quote-4.png)

其实curl URL中加入的单引号并非是curl内部实现的问题，而是bash的实现决定的。

```bash
➜  ~ echo k=x&b=yyy
[1] 15207
k=x                                                                                                                                                                                          
[1]  + 15207 done       echo k=x
➜  ~ echo 'k=x&b=yyy'
k=x&b=yyy
```

那么bash中的单引号到底有什么作用呢？

## Bash 单引号

[引用bash文档](http://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html)

> 3.1.2.2 Single Quotes
> Enclosing characters in single quotes (‘'’) preserves the literal value of each character within the quotes. A single quote may not occur between single quotes, even when preceded by a backslash.
> 
> 3.1.2.3 Double Quotes
> Enclosing characters in double quotes (‘"’) preserves the literal value of all characters within the quotes, with the exception of ‘$’, ‘`’, ‘\’, and, when history expansion is enabled, ‘!’. When the shell is in POSIX mode (see Bash POSIX Mode), the ‘!’ has no special meaning within double quotes, even when history expansion is enabled. The characters ‘$’ and ‘`’ retain their special meaning within double quotes (see Shell Expansions). The backslash retains its special meaning only when followed by one of the following characters: ‘$’, ‘`’, ‘"’, ‘\’, or newline. Within double quotes, backslashes that are followed by one of these characters are removed. Backslashes preceding characters without a special meaning are left unmodified. A double quote may be quoted within double quotes by preceding it with a backslash. If enabled, history expansion will be performed unless an ‘!’ appearing in double quotes is escaped using a backslash. The backslash preceding the ‘!’ is not removed.

简言之，单引号中的内容会保持不变，而双引号中的内容可能会被执行替换。

```bash
➜  ~ echo '$(echo hello)'
$(echo hello)
➜  ~ echo "$(echo hello)"
hello
```