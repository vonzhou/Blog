---
title: "使用WatchService监控文件变化"
date: 2017-09-05
draft: false
categories: ["Java"]
tags: [ "Java"]
---


## 场景

系统实现中经常需要能够感知配置文件的变化，然后及时更新上下文。


## 实现方案


* 自己起一个单独线程，定时加载文件，实现较简单，但是无法保证能够实时捕捉文件变化，同时耗CPU
* 使用commons-io中的 FileAlterationObserver，思想和上面类似，对比前后文件列表的变化，触发对应事件
* JDK 1.7提供的WatchService，利用底层文件系统提供的功能

## 使用 WatchService

WatchService用来监控一个目录是否发生改变，但是可以通过 WatchEvent 上下文定位具体文件的变化。具体使用过程中要注意以下两点：

* 文件改变可能会触发两次事件（我的理解：文件内容的变更，元数据的变更），可以通过文件的时间戳来控制
* 在文件变化事件发生后，如果立即读取文件，可能所获内容并不完整，建议的做法判断文件的 length > 0


```java
// 监控文件的变化，重新加载
executor.submit(new Runnable() {
    @Override
    public void run() {
        try {
            final Path path = FileSystems.getDefault().getPath(getMonitorDir());
            System.out.println(path);
            final WatchService watchService = FileSystems.getDefault().newWatchService();
            final WatchKey watchKey = path.register(watchService, StandardWatchEventKinds.ENTRY_MODIFY);
            while (true) {
                final WatchKey wk = watchService.take();
                for (WatchEvent<?> event : wk.pollEvents()) {
                    final Path changed = (Path) event.context();
                    Path absolute = path.resolve(changed);
                    File configFile = absolute.toFile();
                    long lastModified = configFile.lastModified();
                    logger.info(lastModified + "----------------");
                    // 利用文件时间戳，防止触发两次
                    if (changed.endsWith(getLicenseName()) && lastModified != LAST_MOD && configFile.length > 0) {
                        logger.info("----------------- reloading -----------------");
                        LAST_MOD = lastModified; // 保存上一次时间戳
                        UPDATED = true; // 设置标志位
                    }
                }

                if (LICENSE_UPDATED) {
                    reloadFile(); // 重新加载
                }
                // reset the key
                boolean valid = wk.reset();
                if (!valid) {
                    logger.error("watch key invalid!");
                }
            }
        } catch (Exception e) {
            logger.error("");
        }
    }
});
```

## 参考

[Watching a Directory for Changes](https://docs.oracle.com/javase/tutorial/essential/io/notification.html#concerns)