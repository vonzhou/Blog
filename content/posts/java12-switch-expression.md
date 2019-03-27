---
title: "JDK 12新特性：Switch表达式"
date: 2019-03-20
draft: false
categories: ["Java"]
tags: ["Java", "模式匹配"]
---

JDK 12 GA在2019.3.19发布，其中一项新特性是JEP 325：Switch表达式（Switch Expressions）。学习下。

如果知道Scala中的模式匹配，就很容易理解Switch表达式。

本文完整代码见[SwitchDemo ](https://github.com/vonzhou/learning-java12/blob/master/src/main/java/com/vonzhou/learningjava12/SwitchDemo.java)。

## 传统的Switch语句

传统的Switch语句（switch statement）我们并不陌生，在每个case分支中实现对应的处理逻辑。

```java
private static void switchStatement(WeekDay day) {
    int numLetters = 0;
    switch (day) {
        case MONDAY:
        case FRIDAY:
        case SUNDAY:
            numLetters = 6;
            break;
        case TUESDAY:
            numLetters = 7;
            break;
        case THURSDAY:
        case SATURDAY:
            numLetters = 8;
            break;
        case WEDNESDAY:
            numLetters = 9;
            break;
    }
    System.out.println("1. Num Of Letters: " + numLetters);
}
```

Switch语句的特点是每个case分支块是没有返回值的，而表达式（expression）的特点是有返回值。


## Switch表达式


### 模式匹配（Patrern Matching）

上述“计算字符个数”的例子使用Switch表达式，代码如下：

```java
private static void switchExpression(WeekDay day) {
    int numLetters = switch (day) {
        case MONDAY, FRIDAY, SUNDAY -> 6;
        case TUESDAY -> 7;
        case THURSDAY, SATURDAY -> 8;
        case WEDNESDAY -> 9;
    };

    System.out.println("2. Num Of Letters: " + numLetters);
}
```

Switch表达式目前属于预览（Preview）功能，所以在编译运行的时候需要通过` --enable-preview`选项设置来开启，具体方法如下：

```java
D:\GitHub\learning-java12\src\main\java
λ D:\dev\jdk-12\bin\javac.exe --enable-preview --release 12 com\vonzhou\learningjava12\SwitchDemo.java
注: com\vonzhou\learningjava12\SwitchDemo.java 使用预览语言功能。
注: 有关详细信息，请使用 -Xlint:preview 重新编译。

D:\GitHub\learning-java12\src\main\java
λ D:\dev\jdk-12\bin\java.exe --enable-preview com.vonzhou.learningjava12.SwitchDemo
1. Num Of Letters: 6
2. Num Of Letters: 9
3. Num Of Letters: 8
```

### break 可以返回值

Switch表达式中也支持break有返回值。

```java
private static void switchExpressionBreakReturn(WeekDay day) {
    int numLetters = switch (day) {
        case MONDAY:
        case FRIDAY:
        case SUNDAY:
            break 6;
        case TUESDAY:
            break 7;
        case THURSDAY:
        case SATURDAY:
            numLetters = 8;
            break 8;
        case WEDNESDAY:
            break 9;
    };

    System.out.println("3. Num Of Letters: " + numLetters);
}
```

## Scala中的模式匹配

Scala中实现模式匹配的语法是Match表达式，其实可以看做是Java中的Switch表达式。例如判断一个列表的第一个元素是否是0，可以实现为：

```Scala
def startsWithZero(expr: List[Int]) =
expr match {
  case List(0, _*) => println("found it")
  case _ =>
}
```

## 总结

Switch表达式可以使得写出的代码更加简洁安全（more concisely and safely）。

## 参考

[JEP 325: Switch Expressions (Preview)](https://openjdk.java.net/jeps/325)








