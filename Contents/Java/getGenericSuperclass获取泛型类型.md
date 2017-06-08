# getGenericSuperclass获取泛型类型

`java.lang.Class#getGenericSuperclass`方法的Demo：

```java
public class GenericType {
    static class Base<T> {
    }

    static class Sub<T> extends Base<T> {
    }

    public static void main(String[] args) {
        Sub<String> sub = new Sub<String>();
        Type type = sub.getClass().getGenericSuperclass();
        System.out.println(type);

        // 获取类型参数
        Type paraType = ((ParameterizedType) type).getActualTypeArguments()[0];
        System.out.println(paraType);

        Base base = new Base<Map<String, String>>() {
        };
        System.out.println(((ParameterizedType) base.getClass().getGenericSuperclass()).getActualTypeArguments()[0]);

        System.out.println(new Object().getClass().getGenericSuperclass()); // null
    }
}
```

执行输出：

```java
com.vonzhou.GenericType.com.vonzhou.GenericType$Base<T>
T
java.util.Map<java.lang.String, java.lang.String>
null
```

相关源码，guice的`com.google.inject.TypeLiteral#getSuperclassTypeParameter`。

```java
/**
     * Returns the type from super class's type parameter in {@link MoreTypes#canonicalize(Type)
     * canonical form}.
     */
static Type getSuperclassTypeParameter(Class<?> subclass) {
    Type superclass = subclass.getGenericSuperclass();
    if (superclass instanceof Class) {
        throw new RuntimeException("Missing type parameter.");
    }
    ParameterizedType parameterized = (ParameterizedType) superclass;
    return canonicalize(parameterized.getActualTypeArguments()[0]);
}
```