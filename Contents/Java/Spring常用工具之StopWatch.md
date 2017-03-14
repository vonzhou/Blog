# Spring 常用工具之 StopWatch

##  场景

在平时的开发阶段对一些耗时的操作同时需要进行时间统计的操作，一般会这么做：

```java
private static void doTasks() {
    long start = System.currentTimeMillis();
    task1();
    long end1 = System.currentTimeMillis();
    System.out.println("Task1 Time Cost = " + (end1 - start));
    task2();
    long end2 = System.currentTimeMillis();
    System.out.println("Task2 Time Cost = " + (end2 - end1));
    // ......
}
```

虽然能够满足需求，但是看起来不够美观。在Spring中引入的StopWatch可以使用起来！

## StopWatch

org.springframework.util.StopWatch在文档中解释的已经很清晰了。

> Simple stop watch(秒表), allowing for timing of a number of tasks, exposing total running time and running time for each named task. Conceals(掩盖) use of System.currentTimeMillis(), improving the readability of application code and reducing the likelihood of calculation errors. Note that this object is not designed to be thread-safe and does not use synchronization. This class is normally used to verify performance during proof-of-concepts and in development, rather than as part of production applications.

用法举例：

```java
public void doTasks() {
    StopWatch stopWatch = new StopWatch();
    stopWatch.start("Task1");
    task1();
    stopWatch.stop();
    
    stopWatch.start("Task2");
    task2();
    stopWatch.stop();
    
    System.out.println("Cost = " + stopWatch.getTotalTimeMillis());
    //System.out.println(stopWatch.getLastTaskInfo().getTaskName());
    System.out.println(stopWatch.prettyPrint());
    }
    
    private void task1() {
    System.out.println("task1111111111111111111111111111111111");
    try {
        Thread.sleep(2000);
    } catch (InterruptedException e) {
        ;
    }
    }
    
    private void task2() {
    System.out.println("task22222222222222222222222222222222222");
    try {
        Thread.sleep(3000);
    } catch (InterruptedException e) {
        ;
    }
}
```
执行结果：

```bash
task1111111111111111111111111111111111
task22222222222222222222222222222222222
Cost = 5000
StopWatch '': running time (millis) = 5000
-----------------------------------------
ms     %     Task name
-----------------------------------------
02000  040%  Task1
03000  060%  Task2
```

## 总结

* 常用的工具类善于总结