---
title: "《快学Scala》读书笔记"
date: 2018-12-31
draft: false
categories: ["Scala"]
tags: [ "Scala", "读书"]
---

这本书我是2013年买的，当时看了一部分，然后又忘了，现在重新阅读。

Scala将OOP和函数式编程有机结合，动静兼备。前面的基本招式通读后，基本上可以理解。但是后面的类型系统，协变型变，定界延续目前还搞不懂，暂时略过。


## 1.基础

Scala解释器的使用。

val,var声明值和变量。

有7中数值类型：Byte,Char,Short,Int,Long,Float,Double,Boolean，和Java不同的是这些都是类。

Scala中使用方法进行数值类型的转换，而不是强制类型转换。

和`Java，C++`不同的是，Scala中没有++,--操作符，要使用+=1。

`()`操作符背后的实现原理是`apply`方法。


## 2.控制结构和函数 

if表达式有值。

{}块也有值，值是最后一个表达式的值。这个特性对于要分多步来初始化val的情况很有用。


Unit等同于Java，C++中的void。

赋值语句本身没有值，是Unit。

定义函数的时候，最好不使用return。

Scala中没有Checked Exception。



## 3.数组相关操作 

定长数组是Array, 变长数组是ArrayBuffer。

用 `for(e <- arr)` 遍历元素。

用 `for(e <- arr if ...) yield ...` 转换数组。 

Scala数组和Java数组互操作。

## 4.映射和元组 

Scala中没有可变的树形映射，可以选择Java的TreeMap。

元组可以用于函数需要返回不止一个值的情况。

## 5.类

Scala为每个字段生成`getter，setter`方法，不过可以通过`private,val,var,private[this]`控制这个过程。

如果需要JavaBeans版的`getter，setter`方法，可以使用BeanProperty注解。

Scala中类有一个主构造器（primary constructor），任意多个辅助构造器（auxiliary constructor），名称是this。每个辅助构造器都必须开始于调用其他辅助构造器或者主构造器。


练习5.注意BeanProperty包路径变了，`scala.beans.BeanProperty`。

```java
➜  ch05 git:(master) scalac Student.scala  
➜  ch05 git:(master) javap -private Student
Compiled from "Student.scala"
public class Student {
  private java.lang.String name;
  private long id;
  public java.lang.String name();
  public void name_$eq(java.lang.String);
  public void setName(java.lang.String);
  public long id();
  public void id_$eq(long);
  public void setId(long);
  public java.lang.String getName();
  public long getId();
  public Student(java.lang.String, long);
}
```

## 6.对象

在Java中会使用单例对象的地方，Scala中用对象，单例模式。

搞清类和伴生对象（companion object）的关系。

定义枚举的方法。

## 7.包和引入

包对象（package object）。

可以在任何地方声明包引入。



## 8.继承

要知道Scala的继承层级。

能看懂，但是自己怕是写不出来，需要练习。


## 9.文件和正则表达式

用完Source对象，要记得close。

如果要查看某个字符，但是不处理掉它，使用source.buffered方法（类似C++中的`istream::peek`，或java中的`PushbackInputStream`）。

Scala没有提供读取二进制文件的方法，要使用java类库。写文件也要使用java库`java.io.PrintWriter`。

可以编写shell脚本。

## 10.特质

Scala和Java不能多重继承（菱形继承问题）。

特质可以同时拥有抽象方法和具体方法，类可以实现多个特质。

实现特质用的extends，而不是implements，实现多个特质用with（奇怪么? `extends A with B`，`A with B`先是一个整体，然后由类扩展）。所有Java接口都可作为Scala的trait使用。

注意引入特质后，类的构造器执行顺序。


特质不能有构造器参数。


自身类型（self type）可以解决特质间的循环依赖。


## 11.操作符

操作符的优先级。

apply, update可以简化方法的调用。

unapply，unapplySeq和模式匹配的关系。

## 12.高阶函数

函数是一等公民。

## 13.集合


所有集合都扩展自Iterable trait。

Java中ArrayList和LinkedList实现了共同的List接口，使得编写要考虑随机访问效率的代码比较困难，后来加入的RandomAccess（1.4）就是应对这个的。

Scala优先采用不可变集合。



## 14.模式匹配和样例类

Scala中模式匹配match无需在每个分支后面break。

支持守卫，而无需把每种情况的case都列出来。

倾向于使用类型模式匹配，而不是isInstanceOf操作符。匹配发生在运行时，所以泛型会擦除。

模式匹配用于数组，列表，元组背后是提取器机制，对应的伴生对象实现unapply，unapplySeq方法。比如Array的：

```scala
/** Called in a pattern match like `{ case Array(x,y,z) => println('3 elements')}`.
   *
   *  @param x the selector value
   *  @return  sequence wrapped in a [[scala.Some]], if `x` is a Seq, otherwise `None`
   */
  def unapplySeq[T](x: Array[T]): Option[IndexedSeq[T]] =
    if (x == null) None else Some(x.toIndexedSeq)
    // !!! the null check should to be necessary, but without it 2241 fails. Seems to be a bug
    // in pattern matcher.  @PP: I noted in #4364 I think the behavior is correct.
```


样例类（`Case Class`）的使用场景和作用。List就是用样例类实现的。


推荐使用Option表示可有可无的东西。

## 15.注解


Annotation，StaticAnnotation, ClassfileAnnotation。


## 17.类型参数

类型变量界定，上界`<:`，下界`>:`。

视图界定`<%`，表示可以隐式转换的情况。

要实例化一个`Array[T]`,需要一个`Manifest[T]`对象，这么复杂？因为JVM中泛型擦除。



## 课后习题编程

[github](https://github.com/vonzhou/ScalaImpatient)


> 读于 2018.12.29 杭州
