# JDK源码阅读-List接口

接口List表征的是有序元素集合，允许重复元素存在，有序意味着和索引有关。

* 父接口中有的方法，为何这里又定义一遍？

```java
public interface List<E> extends Collection<E> {
    // Query Operations
    int size();
    boolean isEmpty();
    boolean contains(Object o);

    Iterator<E> iterator();

    Object[] toArray();
    <T> T[] toArray(T[] a);


    // Modification Operations
    boolean add(E e);
    boolean remove(Object o);


    // Bulk Modification Operations
    boolean containsAll(Collection<?> c);
    boolean addAll(Collection<? extends E> c);
    boolean addAll(int index, Collection<? extends E> c);
    boolean removeAll(Collection<?> c);
    boolean retainAll(Collection<?> c);
    
    //since 1.8
    default void replaceAll(UnaryOperator<E> operator) {
        Objects.requireNonNull(operator);
        final ListIterator<E> li = this.listIterator();
        while (li.hasNext()) {
            li.set(operator.apply(li.next()));
        }
    }

   //since 1.8
   // 对排序方法做了包装，先转换为数组，然后sort，而后利用迭代器设置对应的ArrayList
    @SuppressWarnings({"unchecked", "rawtypes"})
    default void sort(Comparator<? super E> c) {
        Object[] a = this.toArray();
        Arrays.sort(a, (Comparator) c);
        ListIterator<E> i = this.listIterator();
        for (Object e : a) {
            i.next();
            i.set((E) e);
        }
    }

    void clear();


    // Comparison and hashing
	boolean equals(Object o);
    int hashCode();


    // Positional Access Operations
    E get(int index);
    E set(int index, E element);
    void add(int index, E element);
    E remove(int index);


    // Search Operations
    int indexOf(Object o);
    int lastIndexOf(Object o);


    // List Iterators
    ListIterator<E> listIterator();
    ListIterator<E> listIterator(int index);

    // View

    List<E> subList(int fromIndex, int toIndex);
}

```