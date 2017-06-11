# Item 8 - equals方法


超类已经覆盖了equals，从超类继承过来的行为对于子类也是合适的话，就不需要覆盖equals方法。比如 AbstractSet，AbstractMap：

```java
/**
 * Compares the specified object with this set for equality.  Returns
 * <tt>true</tt> if the given object is also a set, the two sets have
 * the same size, and every member of the given set is contained in
 * this set.  This ensures that the <tt>equals</tt> method works
 * properly across different implementations of the <tt>Set</tt>
 * interface.<p>
 *
 * This implementation first checks if the specified object is this
 * set; if so it returns <tt>true</tt>.  Then, it checks if the
 * specified object is a set whose size is identical to the size of
 * this set; if not, it returns false.  If so, it returns
 * <tt>containsAll((Collection) o)</tt>.
 *
 * @param o object to be compared for equality with this set
 * @return <tt>true</tt> if the specified object is equal to this set
 */
public boolean equals(Object o) {
    if (o == this)
        return true;

    if (!(o instanceof Set))
        return false;
    Collection<?> c = (Collection<?>) o;
    if (c.size() != size())
        return false;
    try {
        return containsAll(c);
    } catch (ClassCastException unused)   {
        return false;
    } catch (NullPointerException unused) {
        return false;
    }
}
```

```java
/**
 * Compares the specified object with this map for equality.  Returns
 * <tt>true</tt> if the given object is also a map and the two maps
 * represent the same mappings.  More formally, two maps <tt>m1</tt> and
 * <tt>m2</tt> represent the same mappings if
 * <tt>m1.entrySet().equals(m2.entrySet())</tt>.  This ensures that the
 * <tt>equals</tt> method works properly across different implementations
 * of the <tt>Map</tt> interface.
 *
 * @implSpec
 * This implementation first checks if the specified object is this map;
 * if so it returns <tt>true</tt>.  Then, it checks if the specified
 * object is a map whose size is identical to the size of this map; if
 * not, it returns <tt>false</tt>.  If so, it iterates over this map's
 * <tt>entrySet</tt> collection, and checks that the specified map
 * contains each mapping that this map contains.  If the specified map
 * fails to contain such a mapping, <tt>false</tt> is returned.  If the
 * iteration completes, <tt>true</tt> is returned.
 *
 * @param o object to be compared for equality with this map
 * @return <tt>true</tt> if the specified object is equal to this map
 */
public boolean equals(Object o) {
    if (o == this)
        return true;

    if (!(o instanceof Map))
        return false;
    Map<?,?> m = (Map<?,?>) o;
    if (m.size() != size())
        return false;

    try {
        Iterator<Entry<K,V>> i = entrySet().iterator();
        while (i.hasNext()) {
            Entry<K,V> e = i.next();
            K key = e.getKey();
            V value = e.getValue();
            if (value == null) {
                if (!(m.get(key)==null && m.containsKey(key)))
                    return false;
            } else {
                if (!value.equals(m.get(key)))
                    return false;
            }
        }
    } catch (ClassCastException unused) {
        return false;
    } catch (NullPointerException unused) {
        return false;
    }

    return true;
}
```

"值类"需要覆盖equals方法。比如Integer和Date类：

```java
/**
 * Compares this object to the specified object.  The result is
 * {@code true} if and only if the argument is not
 * {@code null} and is an {@code Integer} object that
 * contains the same {@code int} value as this object.
 *
 * @param   obj   the object to compare with.
 * @return  {@code true} if the objects are the same;
 *          {@code false} otherwise.
 */
public boolean equals(Object obj) {
    if (obj instanceof Integer) {
        return value == ((Integer)obj).intValue();
    }
    return false;
}
```

```java
/**
 * Compares two dates for equality.
 * The result is <code>true</code> if and only if the argument is
 * not <code>null</code> and is a <code>Date</code> object that
 * represents the same point in time, to the millisecond, as this object.
 * <p>
 * Thus, two <code>Date</code> objects are equal if and only if the
 * <code>getTime</code> method returns the same <code>long</code>
 * value for both.
 *
 * @param   obj   the object to compare with.
 * @return  <code>true</code> if the objects are the same;
 *          <code>false</code> otherwise.
 * @see     java.util.Date#getTime()
 */
public boolean equals(Object obj) {
    return obj instanceof Date && getTime() == ((Date) obj).getTime();
}
```

覆盖equals方法通用的约定，可以看Object的equals方法说明：

```java
/**
 * Indicates whether some other object is "equal to" this one.
 * <p>
 * The {@code equals} method implements an equivalence relation
 * on non-null object references:
 * <ul>
 * <li>It is <i>reflexive</i>: for any non-null reference value
 *     {@code x}, {@code x.equals(x)} should return
 *     {@code true}.
 * <li>It is <i>symmetric</i>: for any non-null reference values
 *     {@code x} and {@code y}, {@code x.equals(y)}
 *     should return {@code true} if and only if
 *     {@code y.equals(x)} returns {@code true}.
 * <li>It is <i>transitive</i>: for any non-null reference values
 *     {@code x}, {@code y}, and {@code z}, if
 *     {@code x.equals(y)} returns {@code true} and
 *     {@code y.equals(z)} returns {@code true}, then
 *     {@code x.equals(z)} should return {@code true}.
 * <li>It is <i>consistent</i>: for any non-null reference values
 *     {@code x} and {@code y}, multiple invocations of
 *     {@code x.equals(y)} consistently return {@code true}
 *     or consistently return {@code false}, provided no
 *     information used in {@code equals} comparisons on the
 *     objects is modified.
 * <li>For any non-null reference value {@code x},
 *     {@code x.equals(null)} should return {@code false}.
 * </ul>
 * <p>
 * The {@code equals} method for class {@code Object} implements
 * the most discriminating possible equivalence relation on objects;
 * that is, for any non-null reference values {@code x} and
 * {@code y}, this method returns {@code true} if and only
 * if {@code x} and {@code y} refer to the same object
 * ({@code x == y} has the value {@code true}).
 * <p>
 * Note that it is generally necessary to override the {@code hashCode}
 * method whenever this method is overridden, so as to maintain the
 * general contract for the {@code hashCode} method, which states
 * that equal objects must have equal hash codes.
 *
 * @param   obj   the reference object with which to compare.
 * @return  {@code true} if this object is the same as the obj
 *          argument; {@code false} otherwise.
 * @see     #hashCode()
 * @see     java.util.HashMap
 */
public boolean equals(Object obj) {
    return (this == obj);
}
```


















