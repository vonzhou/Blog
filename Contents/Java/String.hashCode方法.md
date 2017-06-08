
hash(s) = s[0]*31^(n-1) + s[1]*31^(n-2) + ... + s[n-1]

这是一个经典的hash算法。

java.lang.String#hashCode源码：

```java
public int hashCode() {
    int h = hash;
    if (h == 0 && value.length > 0) {
        char val[] = value;

        for (int i = 0; i < value.length; i++) {
            h = 31 * h + val[i];
        }
        hash = h;
    }
    return h;
}
```

jdk 1.7中的Objects.hashCode也是同样的思想，代码同guava。



```java
public static int hash(Object... values) {
    return Arrays.hashCode(values);
}
```

java.util.Arrays#hashCode(java.lang.Object[]):

```java
public static int hashCode(Object a[]) {
    if (a == null)
        return 0;

    int result = 1;

    for (Object element : a)
        result = 31 * result + (element == null ? 0 : element.hashCode());

    return result;
}
```