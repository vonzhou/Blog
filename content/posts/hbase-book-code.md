---
title: 运行《HBase权威指南》书中代码
date: 2018-12-18 20:33:59
categories: ["HBase"]
tags: ["Java", "HBase", "Linux"]
---

结合代码阅读《HBase权威指南》，没有实践就没有发言权。

运行《HBase权威指南》书中[代码](https://github.com/vonzhou/hbase-book)

## 前提

搭建好HBase运行环境。


## 设置环境变量

设置MAVEN_HOME, HBASE_CONF_DIR环境变量：

```
export MAVEN_HOME=/usr/share/maven
export HBASE_CONF_DIR=$HBASE_HOME/conf
```

## 编译代码

编译安装父工程。

在hbase-book下面运行：mvn clean compile  install

```
[INFO] HBase Book ......................................... SUCCESS [  0.384 s]
[INFO] HBase Book Common Code ............................. SUCCESS [ 16.906 s]
[INFO] HBase Book Chapter 3 ............................... SUCCESS [  0.994 s]
[INFO] HBase Book Chapter 4 ............................... SUCCESS [  1.469 s]
[INFO] HBase Book Chapter 5 ............................... SUCCESS [  0.628 s]
[INFO] HBase Book Chapter 6 ............................... SUCCESS [  9.460 s]
[INFO] HBase Book Chapter 7 ............................... SUCCESS [  0.933 s]
[INFO] HBase Book Chapter 8 ............................... SUCCESS [  0.289 s]
[INFO] HBase Book Chapter 9 ............................... SUCCESS [  0.269 s]
[INFO] HBase Book Chapter 11 .............................. SUCCESS [  0.141 s]
[INFO] HBase Book Chapter 12 .............................. SUCCESS [ 11.312 s]
[INFO] HBase Book Chapter 13 .............................. SUCCESS [  4.832 s]
[INFO] HBase URL Shortener ................................ SUCCESS [07:24 min]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 08:12 min
[INFO] Finished at: 2018-12-18T19:24:07+08:00
[INFO] Final Memory: 56M/759M
[INFO] ------------------------------------------------------------------------
```

编译安装common工程。

在hbase-book/common下面：mvn clean install


## 运行实例

以第三章的PutExample为例。

```
storm@ubuntu:~/hbase-book/ch03/bin$ ./run.sh client.PutExample
/usr/share/maven/bin/mvn
 WARN [main] (NativeCodeLoader.java:62) - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:zookeeper.version=3.4.8--1, built on 02/06/2016 03:18 GMT
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:host.name=ubuntu
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.version=1.8.0_191
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.vendor=Oracle Corporation
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.class.path=:/home/storm/hbase-book/ch03/bin/../target/classes:/home/storm/.m2/repository/com/larsgeorge/hbase-book-common/2.0/hbase-book-common-2.0.jar:/home/storm/.m2/repository/org/apache/hadoop/hadoop-hdfs/2.7.2/hadoop-hdfs-2.7.2.jar:/home/storm/.m2/repository/org/mortbay/jetty/jetty/6.1.26/jetty-6.1.26.jar:/home/storm/.m2/repository/org/mortbay/jetty/jetty-util/6.1.26/jetty-util-6.1.26.jar:/home/storm/.m2/repository/com/sun/jersey/jersey-core/1.9/jersey-core-1.9.jar:/home/storm/.m2/repository/com/sun/jersey/jersey-server/1.9/jersey-server-1.9.jar:/home/storm/.m2/repository/asm/asm/3.1/asm-3.1.jar:/home/storm/.m2/repository/commons-cli/commons-cli/1.2/commons-cli-1.2.jar:/home/storm/.m2/repository/commons-io/commons-io/2.4/commons-io-2.4.jar:/home/storm/.m2/repository/commons-daemon/commons-daemon/1.0.13/commons-daemon-1.0.13.jar:/home/storm/.m2/repository/log4j/log4j/1.2.17/log4j-1.2.17.jar:/home/storm/.m2/repository/javax/servlet/servlet-api/2.5/servlet-api-2.5.jar:/home/storm/.m2/repository/xmlenc/xmlenc/0.52/xmlenc-0.52.jar:/home/storm/.m2/repository/io/netty/netty/3.6.2.Final/netty-3.6.2.Final.jar:/home/storm/.m2/repository/xerces/xercesImpl/2.9.1/xercesImpl-2.9.1.jar:/home/storm/.m2/repository/xml-apis/xml-apis/1.3.04/xml-apis-1.3.04.jar:/home/storm/.m2/repository/org/fusesource/leveldbjni/leveldbjni-all/1.8/leveldbjni-all-1.8.jar:/home/storm/.m2/repository/org/apache/hadoop/hadoop-client/2.7.2/hadoop-client-2.7.2.jar:/home/storm/.m2/repository/org/apache/hadoop/hadoop-common/2.7.2/hadoop-common-2.7.2.jar:/home/storm/.m2/repository/org/apache/hadoop/hadoop-auth/2.7.2/hadoop-auth-2.7.2.jar:/home/storm/.m2/repository/org/apache/hadoop/hadoop-annotations/2.7.2/hadoop-annotations-2.7.2.jar:/home/storm/.m2/repository/org/apache/zookeeper/zookeeper/3.4.8/zookeeper-3.4.8.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-client/1.3.0/hbase-client-1.3.0.jar:/home/storm/.m2/repository/com/yammer/metrics/metrics-core/2.2.0/metrics-core-2.2.0.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-common/1.3.0/hbase-common-1.3.0.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-protocol/1.3.0/hbase-protocol-1.3.0.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-server/1.3.0/hbase-server-1.3.0.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-procedure/1.3.0/hbase-procedure-1.3.0.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-common/1.3.0/hbase-common-1.3.0-tests.jar:/home/storm/.m2/repository/org/apache/hbase/hbase-annotations/1.3.0/hbase-annotations-1.3.0.jar:/usr/lib/jvm/java-8-openjdk-amd64/lib/tools.jar:/home/storm/.m2/repository/org/apache/htrace/htrace-core/3.1.0-incubating/htrace-core-3.1.0-incubating.jar:/home/storm/.m2/repository/io/netty/netty-all/4.0.23.Final/netty-all-4.0.23.Final.jar:/home/storm/.m2/repository/com/google/protobuf/protobuf-java/2.6.1/protobuf-java-2.6.1.jar:/home/storm/.m2/repository/com/google/guava/guava/15.0/guava-15.0.jar:/home/storm/.m2/repository/org/codehaus/jackson/jackson-mapper-asl/1.9.13/jackson-mapper-asl-1.9.13.jar:/home/storm/.m2/repository/org/codehaus/jackson/jackson-core-asl/1.9.13/jackson-core-asl-1.9.13.jar:/home/storm/.m2/repository/commons-lang/commons-lang/2.6/commons-lang-2.6.jar:/home/storm/.m2/repository/commons-collections/commons-collections/3.2.1/commons-collections-3.2.1.jar:/home/storm/.m2/repository/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:/home/storm/.m2/repository/commons-configuration/commons-configuration/1.10/commons-configuration-1.10.jar:/home/storm/.m2/repository/commons-logging/commons-logging/1.2/commons-logging-1.2.jar:/home/storm/.m2/repository/org/slf4j/slf4j-api/1.7.10/slf4j-api-1.7.10.jar:/home/storm/.m2/repository/org/slf4j/slf4j-simple/1.7.10/slf4j-simple-1.7.10.jar:/home/storm/.m2/repository/ch/qos/logback/logback-core/1.1.2/logback-core-1.1.2.jar:/home/storm/.m2/repository/com/google/code/findbugs/annotations/1.3.9/annotations-1.3.9.jar
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.io.tmpdir=/tmp
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:java.compiler=<NA>
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:os.name=Linux
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:os.arch=amd64
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:os.version=4.15.0-36-generic
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:user.name=storm
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:user.home=/home/storm
[main] INFO org.apache.zookeeper.ZooKeeper - Client environment:user.dir=/home/storm/hbase-book/ch03/bin
[main] INFO org.apache.zookeeper.ZooKeeper - Initiating client connection, connectString=localhost:2181 sessionTimeout=90000 watcher=org.apache.hadoop.hbase.zookeeper.PendingWatcher@2b546384
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Opening socket connection to server dev/127.0.1.1:2181. Will not attempt to authenticate using SASL (unknown error)
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Socket connection established to dev/127.0.1.1:2181, initiating session
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Session establishment complete on server dev/127.0.1.1:2181, sessionid = 0x100000ae61d0081, negotiated timeout = 40000
[main] INFO org.apache.zookeeper.ZooKeeper - Initiating client connection, connectString=localhost:2181 sessionTimeout=90000 watcher=org.apache.hadoop.hbase.zookeeper.PendingWatcher@7e5afaa6
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Opening socket connection to server dev/127.0.1.1:2181. Will not attempt to authenticate using SASL (unknown error)
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Socket connection established to dev/127.0.1.1:2181, initiating session
[main-SendThread(dev:2181)] INFO org.apache.zookeeper.ClientCnxn - Session establishment complete on server dev/127.0.1.1:2181, sessionid = 0x100000ae61d0082, negotiated timeout = 40000
[main] INFO org.apache.zookeeper.ZooKeeper - Session: 0x100000ae61d0082 closed
[main-EventThread] INFO org.apache.zookeeper.ClientCnxn - EventThread shut down for session: 0x100000ae61d0082
[main-EventThread] INFO org.apache.zookeeper.ClientCnxn - EventThread shut down for session: 0x100000ae61d0081
[main] INFO org.apache.zookeeper.ZooKeeper - Session: 0x100000ae61d0081 closed
```


## 验证 

可以用hbase shell验证数据已经插入了。

```
storm@ubuntu:~/dev/hbase-1.2.2/bin$ ./hbase shell
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/home/storm/dev/hbase-1.2.2/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/home/storm/dev/hadoop-2.8.5/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
HBase Shell; enter 'help<RETURN>' for list of supported commands.
Type "exit<RETURN>" to leave the HBase Shell
Version 1.2.2, r3f671c1ead70d249ea4598f1bbcc5151322b3a13, Fri Jul  1 08:28:55 CDT 2016

hbase(main):001:0> list
TABLE                                                                                                                                                                                        
test                                                                                                                                                                                         
testtable                                                                                                                                                                                    
2 row(s) in 0.1770 seconds

=> ["test", "testtable"]
hbase(main):002:0> scan 'testtable'
ROW                                              COLUMN+CELL                                                                                                                                 
 row1                                            column=colfam1:qual1, timestamp=1545134760590, value=val1                                                                                   
 row1                                            column=colfam1:qual2, timestamp=1545134760590, value=val2                                                                                   
1 row(s) in 0.1740 seconds
```