# JDK源码阅读-Collection 


集合类的顶级接口，定义了集合的基本行为，高度抽象。


```java

public interface Collection<E> extends Iterable<E> {
    // Query Operations

    int size();
    boolean isEmpty();
    boolean contains(Object o);
    Iterator<E> iterator();
    Object[] toArray();
    // 这个要好好理解下
    <T> T[] toArray(T[] a);

    // Modification Operations
    
    boolean add(E e);
    boolean remove(Object o);


    // Bulk Operations  批量操作

    boolean containsAll(Collection<?> c);
    boolean addAll(Collection<? extends E> c);
    boolean removeAll(Collection<?> c);

    // since 1.8
    default boolean removeIf(Predicate<? super E> filter) {
        Objects.requireNonNull(filter);
        boolean removed = false;
        final Iterator<E> each = iterator();
        while (each.hasNext()) {
            if (filter.test(each.next())) {
                each.remove();
                removed = true;
            }
        }
        return removed;
    }

   
    boolean retainAll(Collection<?> c);

    void clear();


    // Comparison and hashing

    boolean equals(Object o);
    int hashCode();

    // since 1.8 对于Stream有待研究
    
    @Override
    default Spliterator<E> spliterator() {
        return Spliterators.spliterator(this, 0);
    }

   
    default Stream<E> stream() {
        return StreamSupport.stream(spliterator(), false);
    }

    
    default Stream<E> parallelStream() {
        return StreamSupport.stream(spliterator(), true);
    }
}
```

继承Collection的常用接口有List, Set, Deque等，容器变得更具体了。

[Set interface](javainternals-Set.md)

[List interface](javainternals-List.md)

[SortedSet interface]()
