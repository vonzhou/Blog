# 关于 ArrayList.toArray() 和 Arrays.asList().toArray()方法

最近在项目中调用一个接口, 接口的返回类型是 `Map<String, Object>`，且put进去的值类型是`List<Dog>`，当我取出进行强制类型转化的时候却抛出了`ClassCastException`，情景如下：

```java
public static void test2() {
    List<String> list = new ArrayList<>();
    list.add("dog");

    Object[] oa = list.toArray();//其实此时数组类型已为 [Ljava.lang.Object;
    System.out.println(((String) oa[0]).length());
    String[] sa = (String[]) oa; // 所以此时会抛出 ClassCastException
}
```

原因是ArrayList.toArray方法返回的是Object[]，String[]类型和Object[]类型是不同的，虽然List中的元素具体类型是String。

```java
/**
 * The array buffer into which the elements of the ArrayList are stored.
 * The capacity of the ArrayList is the length of this array buffer. Any
 * empty ArrayList with elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA
 * will be expanded to DEFAULT_CAPACITY when the first element is added.
 */
transient Object[] elementData; // non-private to simplify nested class access

/**
 * Returns an array containing all of the elements in this list
 * in proper sequence (from first to last element).
 *
 * <p>The returned array will be "safe" in that no references to it are
 * maintained by this list.  (In other words, this method must allocate
 * a new array).  The caller is thus free to modify the returned array.
 *
 * <p>This method acts as bridge between array-based and collection-based
 * APIs.
 *
 * @return an array containing all of the elements in this list in
 *         proper sequence
 */
public Object[] toArray() {
    return Arrays.copyOf(elementData, size);
}
```

值得注意的是ArrayList底层存储是 Object[]类型的elementData，虽然Arrays.copyOf方法返回的其实是原始数组的真实类型。

Arrays:

```java
/**
 * Copies the specified array, truncating or padding with nulls (if necessary)
 * so the copy has the specified length.  For all indices that are
 * valid in both the original array and the copy, the two arrays will
 * contain identical values.  For any indices that are valid in the
 * copy but not the original, the copy will contain <tt>null</tt>.
 * Such indices will exist if and only if the specified length
 * is greater than that of the original array.
 * The resulting array is of exactly the same class as the original array.
 *
 * @param <T> the class of the objects in the array
 * @param original the array to be copied
 * @param newLength the length of the copy to be returned
 * @return a copy of the original array, truncated or padded with nulls
 *     to obtain the specified length
 * @throws NegativeArraySizeException if <tt>newLength</tt> is negative
 * @throws NullPointerException if <tt>original</tt> is null
 * @since 1.6
 */
@SuppressWarnings("unchecked")
public static <T> T[] copyOf(T[] original, int newLength) {
    return (T[]) copyOf(original, newLength, original.getClass());
}
```


但是如果我们使用 `Arrays.asList` 就不会出现上述的问题。

```java
public static void test1() {
    List<String> list = Arrays.asList("hello");

    System.out.println(list.toArray().getClass());

    Object[] oa = list.toArray();
    String[] sa = (String[]) oa;// ok
}
```

因为Arrays.asList返回的不是ArrayList，而不是一个内部类java.util.Arrays.ArrayList，底层存储类型是泛型类型数组。具体：

```java
private static class ArrayList<E> extends AbstractList<E>
    implements RandomAccess, java.io.Serializable
{
    private static final long serialVersionUID = -2764017481108945198L;
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

对于 `java.util.ArrayList` 我们可以使用 `toArray(T[] a)` 方法来返回指定返回数组的类型,这也是推荐的方式。

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


