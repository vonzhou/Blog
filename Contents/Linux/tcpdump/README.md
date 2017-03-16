# tcpdump 常用命令整理
---

tcpdump使用libpcap库，在网络层实现抓包，然后可以供我们分析。

-i 指定在某个interface进行抓包。

![](tcpdump-i.png)

-n 数字形式展示主机和服务端口。

-c 指定抓包的数目。

![](tcpdump-c.png)

-s 可以设置抓取包的大小，-s0则表示capture the whole packet.

![](tcpdump-s.png)

-e 可以显示MAC地址，协议类型。

![](tcpdump-e.png)

-v 会得到详细（verbose）信息（v,vv,vvv逐渐增多）.

![](tcpdump-v.png)

-S 显示TCP的绝对序列号，而不是相对于初始序列号(ISN的相对值。

![](tcpdump-S.png)

-w 用于指定文件存储抓取的包。

![](tcpdump-w.png)

-r 用于读取我们刚才保存的文件。

![](tcpdump-w.png)

port XX 指定具体的端口。

![](tcpdump-port.png)

在网络程序的调试中要善于利用上述选项的组合进行分析！













