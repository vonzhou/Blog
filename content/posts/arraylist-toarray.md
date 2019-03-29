---
title: "关于 ArrayList.toArray() 和 Arrays.asList().toArray()方法"
date: 2017-02-18
draft: false
categories: ["Java"]
tags: [ "Java", "String"]
---


## 引言

最近在项目中调用一个接口, 接口的返回类型是 `Map<String, Object>`，且put进去的值类型是`List<Dog>`，当我取出进行强制类型转化的时候却抛出了`ClassCastException`，情景如下：

```java
public static void test2() {
    List<Dog> list = new ArrayList<>();
    list.add(new Dog());
    System.out.println(list.toArray().getClass()); // 其实此时数组类型已为 [Ljava.lang.Object;

    Map<String, Object> dataMap = Maps.newHashMap();
    dataMap.put("x", list.toArray());
    Dog[] d = (Dog[]) dataMap.get("x"); // 所以此时会抛出 ClassCastException
}
```

所以在使用toArray方法的时候要确实理解。

## ArrayList.toArray() 理解

通过源码我们可以看到返回的是Object类型的数组，失去了原有的实际类型，虽然底层存储是具体类型的对象，这也正体现了文档中说的：该方法起到了bridge的作用（This method acts as bridge between array-based and collection-based APIs）。

```java
public Object[] toArray() {
    return Arrays.copyOf(elementData, size);
}
```

但是如果我们使用 Arrays.asList 就不会出现上述的问题。

```java
public static void test1() {
    List<Dog> list = Arrays.asList(new Dog(), new BigDog());

    System.out.println(list.toArray().getClass());

    Map<String, Object> dataMap = Maps.newHashMap();
    dataMap.put("x", list.toArray());
    Dog[] d = (Dog[]) dataMap.get("x");
}
```

对于 java.util.ArrayList 我们可以使用 toArray(T[] a) 方法来返回指定返回数组的类型。

```java
public <T> T[] toArray(T[] a) {
    if (a.length < size)
        // Make a new array of a's runtime type, but my contents:
        return (T[]) Arrays.copyOf(elementData, size, a.getClass());
    System.arraycopy(elementData, 0, a, 0, size);
    if (a.length > size)
        a[size] = null;
    return a;
}
```

## Arrays.asList().toArray()理解

工具类Arrays的asList()方法实际中经常会用到，用于把指定的对象包装成一个固定大小的对象数组，但是其返回的ArrayList是其内部类，不同于java.util.ArrayList。

```java
public static <T> List<T> asList(T... a) {
    return new ArrayList<>(a);
}

private static class ArrayList<E> extends AbstractList<E>
    implements RandomAccess, java.io.Serializable
{
    private static final long serialVersionUID = -2764017481108945198L;
    // 实际存储有保留原始类型
    private final E[] a;

    ArrayList(E[] array) {
        a = Objects.requireNonNull(array);
    }

    @Override
    public int size() {
        return a.length;
    }

    @Override
    public Object[] toArray() {
        return a.clone();
    }

    @Override
    @SuppressWarnings("unchecked")
    public <T> T[] toArray(T[] a) {
        int size = size();
        if (a.length < size)
            return Arrays.copyOf(this.a, size,
                                 (Class<? extends T[]>) a.getClass());
        System.arraycopy(this.a, 0, a, 0, size);
        if (a.length > size)
            a[size] = null;
        return a;
    }

    @Override
    public E get(int index) {
        return a[index];
    }

    @Override
    public E set(int index, E element) {
        E oldValue = a[index];
        a[index] = element;
        return oldValue;
    }

    @Override
    public int indexOf(Object o) {
        E[] a = this.a;
        if (o == null) {
            for (int i = 0; i < a.length; i++)
                if (a[i] == null)
                    return i;
        } else {
            for (int i = 0; i < a.length; i++)
                if (o.equals(a[i]))
                    return i;
        }
        return -1;
    }

    @Override
    public boolean contains(Object o) {
        return indexOf(o) != -1;
    }

    @Override
    public Spliterator<E> spliterator() {
        return Spliterators.spliterator(a, Spliterator.ORDERED);
    }

    @Override
    public void forEach(Consumer<? super E> action) {
        Objects.requireNonNull(action);
        for (E e : a) {
            action.accept(e);
        }
    }

    @Override
    public void replaceAll(UnaryOperator<E> operator) {
        Objects.requireNonNull(operator);
        E[] a = this.a;
        for (int i = 0; i < a.length; i++) {
            a[i] = operator.apply(a[i]);
        }
    }

    @Override
    public void sort(Comparator<? super E> c) {
        Arrays.sort(a, c);
    }
}
```

这里虽然我们看到 toArray 方法返回的依然是 Object[]，但是与 java.util.ArrayList 不同的是这里底层存储是泛型类型的数组 private final E[] a，所以保留了实际的类型，如下：

```java
public static void test5() {
    Object[] objs = new Dog[1];
    System.out.println(objs.getClass()); // 类型是 [Lcom.vonzhou.learn.other.ClassDemo$Dog

    Object[] objs2 = new Object[1];
    objs2[0] = new Dog();
    System.out.println(objs2.getClass()); // 类型是 [Ljava.lang.Object;
}
```

## 总结

类型系统很复杂，这里只是看到了表象。
