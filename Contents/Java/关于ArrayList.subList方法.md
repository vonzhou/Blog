# 关于ArrayList.subList方法


## 直接代码

和Arrays.asList方法类似，ArrayList.subList返回的是其内部类SubList的实例（原始链表的一个视图），所以不能强制转换为ArrayList类型。

```java
public static void test1() {
    ArrayList<String> list = new ArrayList<>();
    list.add("1");
    list.add("2");
    list.add("3");

    List<String> sub = list.subList(0, 1);

    // java.lang.ClassCastException: java.util.ArrayList$SubList cannot be cast to
    // java.util.ArrayList
    ArrayList<String> force = (ArrayList<String>) sub;
}
```

看SubList的源码，也较容易理解。

```java
class SubList<E> extends AbstractList<E> {
    private final AbstractList<E> l;  // 引用原始的宿主 ArrayList
    private final int offset;    // 切片位置
    private int size;
    
    SubList(AbstractList<E> list, int fromIndex, int toIndex) {
        if (fromIndex < 0)
            throw new IndexOutOfBoundsException("fromIndex = " + fromIndex);
        if (toIndex > list.size())
            throw new IndexOutOfBoundsException("toIndex = " + toIndex);
        if (fromIndex > toIndex)
            throw new IllegalArgumentException("fromIndex(" + fromIndex +
                                               ") > toIndex(" + toIndex + ")");
        l = list;
        offset = fromIndex;
        size = toIndex - fromIndex;
        this.modCount = l.modCount;
    }
    
    public E set(int index, E element) {
        rangeCheck(index);     // 检查是否越界
        checkForComodification();    //  检查modCount
        return l.set(index+offset, element);   // 修改操作都是通过原始链表进行
    }
    
    // 其他同理
    
    public List<E> subList(int fromIndex, int toIndex) {
        return new SubList<>(this, fromIndex, toIndex);
    }
}
```

可以看到在SubList的所有方法中都进行了并发修改的检测（`checkForComodification`）。

```java
private void checkForComodification() {
    if (this.modCount != l.modCount)
        throw new ConcurrentModificationException();
}
```

如果修改了原始ArrayList的结构（'structurally modified'），自然会导致该SubList对象和原ArrayList对象的modCount不同。

```java
public static void test3() {
    ArrayList<String> list = new ArrayList<>();
    list.add("1");
    list.add("2");
    list.add("3");

    List<String> sub = list.subList(0, 2); // 是一个视图

    list.remove(0); // 修改原ArrayList的个数
    System.out.println(list); // [2, 3]

    // java.util.ConcurrentModificationException 因为执行subList的时候保存了原ArrayList当时的modCount
    System.out.println(sub.get(0));
}
```

但是通过SubList对链表的结构进行修改，会修改底层的存储，同时更新modCount，所以不会抛出上述的`ConcurrentModificationException`。

```java
public static void test4() {
    ArrayList<String> list = new ArrayList<>();
    list.add("1");
    list.add("2");
    list.add("3");

    List<String> sub = list.subList(0, 2);
    sub.remove("1"); // 可以通过subList提供的方法改变ArrayList的元素个数

    System.out.println(list);
}
```


## 总结

* ArrayList.subList返回是一个内部类对象视图
* 注意结构性的修改带来的`ConcurrentModificationException`