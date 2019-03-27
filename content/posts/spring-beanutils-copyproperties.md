---
title: "BeanUtils.copyProperties 源码分析"
date: 2019-02-27
draft: false
categories: ["Spring"]
tags: ["Java", "Spring"]
---

## 概述

* 利用反射
* 字段不一致也不会报错，因为会根据目标对象的属性去源对象中找对应的属性描述符，存在才拷贝
* 相同字段，类型不同，也不会有问题，因为拷贝之时会判断该字段源对象的读方法返回值，是否可应用用目标对象的写方法参数


## 实例

```java
public class CopyPropertiesDemo {

    public static void main(String[] args) {

        Student s = new Student();
        s.setName("vz");
        s.setFoo(1024);
        s.setBar(-1);

        Father f = new Father();
        BeanUtils.copyProperties(s, f);
        System.out.println(f);
    }

    static class Student{
        private String name;
        private int foo;
        private int bar;
        // setters and getters
    }


    static class Father{
        private String name;
        private int age;
        private int salary;
        private double foo;
        private Integer bar;
        // setters and getters

        @Override
        public String toString() {
            return "Father{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    ", salary=" + salary +
                    ", foo=" + foo +
                    ", bar=" + bar +
                    '}';
        }
    }
}
```


输出：

```
Father{name='vz', age=0, salary=0, foo=0.0, bar=-1}
```

## copyProperties 源码分析


copyProperties 的实现总体上很清晰：利用反射，调用source对象的get方法，然后set到target对象中。


```java
public static void copyProperties(Object source, Object target) throws BeansException {
		copyProperties(source, target, null, (String[]) null);
	}

private static void copyProperties(Object source, Object target, Class<?> editable, String... ignoreProperties)
			throws BeansException {
		Class<?> actualEditable = target.getClass();

		PropertyDescriptor[] targetPds = getPropertyDescriptors(actualEditable);
		List<String> ignoreList = (ignoreProperties != null ? Arrays.asList(ignoreProperties) : null);

		for (PropertyDescriptor targetPd : targetPds) {
			Method writeMethod = targetPd.getWriteMethod();
			if (writeMethod != null && (ignoreList == null || !ignoreList.contains(targetPd.getName()))) {
				PropertyDescriptor sourcePd = getPropertyDescriptor(source.getClass(), targetPd.getName());
				if (sourcePd != null) {
					Method readMethod = sourcePd.getReadMethod();
					if (readMethod != null &&
							ClassUtils.isAssignable(writeMethod.getParameterTypes()[0], readMethod.getReturnType())) {
						try {
							if (!Modifier.isPublic(readMethod.getDeclaringClass().getModifiers())) {
								readMethod.setAccessible(true);
							}
							Object value = readMethod.invoke(source);
							if (!Modifier.isPublic(writeMethod.getDeclaringClass().getModifiers())) {
								writeMethod.setAccessible(true);
							}
							writeMethod.invoke(target, value);
						}
						catch (Throwable ex) {
							throw new FatalBeanException(
									"Could not copy property '" + targetPd.getName() + "' from source to target", ex);
						}
					}
				}
			}
		}
	}

```

## 获取 PropertyDescriptor

PropertyDescriptor 描述的是Java Bean的一个属性，具有读写(getter/setter)方法，


```java
public static PropertyDescriptor[] getPropertyDescriptors(Class<?> clazz) throws BeansException {
		CachedIntrospectionResults cr = CachedIntrospectionResults.forClass(clazz);
		return cr.getPropertyDescriptors();
	}

```

`CachedIntrospectionResults`缓存了Java Bean对应Class的`PropertyDescriptor`信息，存储数据结构是`ConcurrentHashMap`：

```java
static final ConcurrentMap<Class<?>, CachedIntrospectionResults> strongClassCache =
			new ConcurrentHashMap<Class<?>, CachedIntrospectionResults>(64);
```

先从缓存中查询，如果没有，则进行实际的解析，构造。


```java
static CachedIntrospectionResults forClass(Class<?> beanClass) throws BeansException {
		CachedIntrospectionResults results = strongClassCache.get(beanClass);
		if (results != null) {
			return results;
		}
		results = softClassCache.get(beanClass);
		if (results != null) {
			return results;
		}

        // TODO 具体的解析过程
		results = new CachedIntrospectionResults(beanClass);
		ConcurrentMap<Class<?>, CachedIntrospectionResults> classCacheToUse;

        // TODO cachesafe ？
		if (ClassUtils.isCacheSafe(beanClass, CachedIntrospectionResults.class.getClassLoader()) ||
				isClassLoaderAccepted(beanClass.getClassLoader())) {
			classCacheToUse = strongClassCache;
		}
		else {
			classCacheToUse = softClassCache;
		}

		CachedIntrospectionResults existing = classCacheToUse.putIfAbsent(beanClass, results);
		return (existing != null ? existing : results);
	}

```

接下来看`CachedIntrospectionResults`构造函数，先是利用`Introspector`解析class的`BeanInfo`（实现类是`GenericBeanInfo`），然后更新缓存。

```java
private CachedIntrospectionResults(Class<?> beanClass) throws BeansException {
		try {
			BeanInfo beanInfo = null;
			if (beanInfo == null) {
				// If none of the factories supported the class, fall back to the default
				beanInfo = (shouldIntrospectorIgnoreBeaninfoClasses ?
						Introspector.getBeanInfo(beanClass, Introspector.IGNORE_ALL_BEANINFO) :
						Introspector.getBeanInfo(beanClass)); // 这里
			}
			this.beanInfo = beanInfo;


			this.propertyDescriptorCache = new LinkedHashMap<String, PropertyDescriptor>();

			// This call is slow so we do it once.
			PropertyDescriptor[] pds = this.beanInfo.getPropertyDescriptors();
			for (PropertyDescriptor pd : pds) {
				if (Class.class == beanClass &&
						("classLoader".equals(pd.getName()) ||  "protectionDomain".equals(pd.getName()))) {
					// Ignore Class.getClassLoader() and getProtectionDomain() methods - nobody needs to bind to those
					continue;
				}
				pd = buildGenericTypeAwarePropertyDescriptor(beanClass, pd);
				this.propertyDescriptorCache.put(pd.getName(), pd);
			}

			this.typeDescriptorCache = new ConcurrentReferenceHashMap<PropertyDescriptor, TypeDescriptor>();
		}
		catch (IntrospectionException ex) {
			throw new FatalBeanException("Failed to obtain BeanInfo for class [" + beanClass.getName() + "]", ex);
		}
	}

```


## 判断是否可赋值（Assignable）


看工具类`ClassUtils`。



```java
public static boolean isAssignable(Class<?> lhsType, Class<?> rhsType) {
		if (lhsType.isAssignableFrom(rhsType)) {
			return true;
		}
		if (lhsType.isPrimitive()) {
			Class<?> resolvedPrimitive = primitiveWrapperTypeMap.get(rhsType);
			if (lhsType == resolvedPrimitive) {
				return true;
			}
		}
		else {
			Class<?> resolvedWrapper = primitiveTypeToWrapperMap.get(rhsType);
			if (resolvedWrapper != null && lhsType.isAssignableFrom(resolvedWrapper)) {
				return true;
			}
		}
		return false;
	}

```

`java.lang.Class.isAssignableFrom`方法是native的，判断当前类型是否是另一个的超类，或者父接口，或者类型一样，可以看个例子：



```java
public class IsAssignableFromDemo {
    public static void main(String[] args) {
        System.out.println(Object.class.isAssignableFrom(Object.class)); // true
        System.out.println(Object.class.isAssignableFrom(String.class)); // true
        System.out.println(List.class.isAssignableFrom(ArrayList.class)); // true
        System.out.println(int.class.isAssignableFrom(long.class)); //false
        System.out.println(int.class.isAssignableFrom(int.class));//true
    }
}

```

`isAssignable`同时也会考虑原始类型及包装类型的情况，比如 int a 可以被拷贝到另一个对象的 Integer a 中。


