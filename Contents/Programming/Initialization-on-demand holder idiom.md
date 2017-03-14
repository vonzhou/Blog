# Initialization-on-demand holder idiom
---

[From Wikipedia](https://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom)

In software engineering, the Initialization on Demand Holder (design pattern) idiom is a lazy-loaded singleton. In all versions of Java, the idiom enables a safe, highly concurrent lazy initialization with good performance.

```java

public class Something {
    private Something() {}

    private static class LazyHolder {
        private static final Something INSTANCE = new Something();
    }

    public static Something getInstance() {
        return LazyHolder.INSTANCE;
    }
}
```

The implementation of the idiom relies on the initialization phase of execution within the Java Virtual Machine (JVM) as specified by the Java Language Specification (JLS).[2] When the class Something is loaded by the JVM, the class goes through initialization. Since the class does not have any static variables to initialize, the initialization completes trivially. The static class definition LazyHolder within it is not initialized until the JVM determines that LazyHolder must be executed. The static class LazyHolder is only executed when the static method getInstance is invoked on the class Something, and the first time this happens the JVM will load and initialize the LazyHolder class. The initialization of the LazyHolder class results in static variable INSTANCE being initialized by executing the (private) constructor for the outer class Something. Since the class initialization phase is guaranteed by the JLS to be serial, i.e., non-concurrent, no further synchronization is required in the static getInstance method during loading and initialization. And since the initialization phase writes the static variable INSTANCE in a serial operation, all subsequent concurrent invocations of the getInstance will return the same correctly initialized INSTANCE without incurring any additional synchronization overhead.

This gives a highly efficient thread-safe "singleton" cache, without synchronization overhead; benchmarking indicates it to be far faster than even uncontended synchronization.[3] However, the idiom is singleton-specific and not extensible to pluralities of objects (e.g. a map-based cache).

Only One Chance To Initialize

Despite the elegance of this approach (first described by Pugh), any failure to initialize renders the class unusable which means the holder pattern can only be used when the programmer is certain the initialization will not fail. Example:

```java
public class PughFail {
    public static class Something {
        private Something() {
            super();
            System.out.println(this.getClass().getName() + " called");
            if (System.currentTimeMillis() > 0) {
                System.out.println("EMULATING INIT FAILURE");
                throw new RuntimeException("EMULATING INIT FAILURE");
            }
        }
        private static class LazyHolder {
            private static final Something INSTANCE = new Something();
        }
        public static Something getInstance() {
            return LazyHolder.INSTANCE;
        }
    }
    public static void main(String[] args) {
        System.out.println("First try");
        try {
            Something.getInstance();
        } catch (Throwable t) {
            System.out.println(t);
        }
        System.out.println("Second try");
        try {
            Something.getInstance();
        } catch (Throwable t) {
            System.out.println(t);
        }
    }
}
```

output:

```bash
First try
PughFail$Something called
EMULATING INIT FAILURE
java.lang.ExceptionInInitializerError
Second try
java.lang.NoClassDefFoundError: Could not initialize class PughFail$Something$LazyHolder
```