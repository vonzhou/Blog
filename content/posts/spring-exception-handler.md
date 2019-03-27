---
title: "ExceptionHandler 异常处理过程分析"
date: 2017-08-10
draft: false
categories: ["Spring"]
tags: [ "Spring", "Spring MVC"]
---

`ExceptionHandler` 的使用场景就是在 Controller 中捕获异常，全局统一处理，而不是在每个 handler 中都进行繁琐的异常捕获操作，优点就是代码整洁。

![执行流程](/images/spring-exception-handler.jpg)

ExceptionHandler 异常处理过程大体为：执行 handler 方法如果抛出了异常，就根据异常类型查找到对应的异常处理方法，然后执行对应的方法，上图展示了这一过程。下面列出异常处理方法解析的过程。


`getExceptionHandlerMethod` 根据特定的异常找到匹配的 `@ExceptionHandler` 方法，这里只关注在 Controller 查找有 ExceptionHandler 方法的路径，先忽略 ControllerAdvice 的情况。通过如下代码可以看到，对于每一个 handler 都有一个异常处理器缓存（exceptionHandlerCache），局部性原理。初次会进行 ExceptionHandlerMethodResolver 的构造，获取到 ExceptionHandlerMethodResolver 之后，根据异常获取到响应的方法，包装成一个 InvocableHandlerMethod 返回。


```java
protected ServletInvocableHandlerMethod getExceptionHandlerMethod(HandlerMethod handlerMethod, Exception exception) {
	Class<?> handlerType = (handlerMethod != null ? handlerMethod.getBeanType() : null);

	if (handlerMethod != null) {
		ExceptionHandlerMethodResolver resolver = this.exceptionHandlerCache.get(handlerType); // 关键点1
		if (resolver == null) {
			resolver = new ExceptionHandlerMethodResolver(handlerType); // 关键点2
			this.exceptionHandlerCache.put(handlerType, resolver);
		}
		Method method = resolver.resolveMethod(exception); // 关键点3
		if (method != null) {
			return new ServletInvocableHandlerMethod(handlerMethod.getBean(), method);
		}
	}
    // 忽略 ....
	for (Entry<ControllerAdviceBean, ExceptionHandlerMethodResolver> entry : this.exceptionHandlerAdviceCache.entrySet()) {
		if (entry.getKey().isApplicableToBeanType(handlerType)) {
			ExceptionHandlerMethodResolver resolver = entry.getValue();
			Method method = resolver.resolveMethod(exception);
			if (method != null) {
				return new ServletInvocableHandlerMethod(entry.getKey().resolveBean(), method);
			}
		}
	}

	return null;
}
```

## ExceptionHandlerMethodResolver 构造


在 ExceptionHandlerMethodResolver 构造函数中会解析有 ExceptionHandler 注解的方法，然后放置到缓存中，便于根据异常类型获取对应的处理方法。具体地，先看 ExceptionHandler 注解的 value 值，如果没有的话就看异常处理方法的参数中是否有表示异常类型的参数，这样就可以确定这个异常处理方法可以处理哪些异常类型。后续在出现具体异常的时候就可以根据异常类型直接查找这个映射表。


```java
private final Map<Class<? extends Throwable>, Method> mappedMethods =
			new ConcurrentHashMap<Class<? extends Throwable>, Method>(16);
			

public ExceptionHandlerMethodResolver(Class<?> handlerType) {
	for (Method method : MethodIntrospector.selectMethods(handlerType, EXCEPTION_HANDLER_METHODS)) {
		for (Class<? extends Throwable> exceptionType : detectExceptionMappings(method)) {
			addExceptionMapping(exceptionType, method);  // 保存到map中
		}
	}
}

// 确定这个异常处理方法可以处理哪些异常类型
private List<Class<? extends Throwable>> detectExceptionMappings(Method method) {
	List<Class<? extends Throwable>> result = new ArrayList<Class<? extends Throwable>>();
	detectAnnotationExceptionMappings(method, result);  // 关键点1
	if (result.isEmpty()) {
		for (Class<?> paramType : method.getParameterTypes()) {  // 关键点2
			if (Throwable.class.isAssignableFrom(paramType)) {
				result.add((Class<? extends Throwable>) paramType);
			}
		}
	}
	Assert.notEmpty(result, "No exception types mapped to {" + method + "}");
	return result;
}

protected void detectAnnotationExceptionMappings(Method method, List<Class<? extends Throwable>> result) {
	ExceptionHandler ann = AnnotationUtils.findAnnotation(method, ExceptionHandler.class); // 寻找 ExceptionHandler 注解并返回
	result.addAll(Arrays.asList(ann.value()));  // ExceptionHandler 的 value 表示的是要处理的异常类型
}

// 有 @ExceptionHandler 注解的方法过滤器
public static final MethodFilter EXCEPTION_HANDLER_METHODS = new MethodFilter() {
	@Override
	public boolean matches(Method method) {
		return (AnnotationUtils.findAnnotation(method, ExceptionHandler.class) != null);
	}
};
```

## 确定异常的处理方法

可以看到最终是从上述解析到的 mappedMethods 中查找，并且维护一个本地缓存。

```java
public Method resolveMethod(Exception exception) {
	Method method = resolveMethodByExceptionType(exception.getClass());
	if (method == null) {
		Throwable cause = exception.getCause();
		if (cause != null) {
			method = resolveMethodByExceptionType(cause.getClass());
		}
	}
	return method;
}

public Method resolveMethodByExceptionType(Class<? extends Throwable> exceptionType) {
	Method method = this.exceptionLookupCache.get(exceptionType);
	if (method == null) {
		method = getMappedMethod(exceptionType);
		this.exceptionLookupCache.put(exceptionType, (method != null ? method : NO_METHOD_FOUND)); // 缓存
	}
	return (method != NO_METHOD_FOUND ? method : null);
}

private Method getMappedMethod(Class<? extends Throwable> exceptionType) {
	List<Class<? extends Throwable>> matches = new ArrayList<Class<? extends Throwable>>();
	for (Class<? extends Throwable> mappedException : this.mappedMethods.keySet()) { // 最终查找
		if (mappedException.isAssignableFrom(exceptionType)) {
			matches.add(mappedException);
		}
	}
	if (!matches.isEmpty()) {
		Collections.sort(matches, new ExceptionDepthComparator(exceptionType));  // 有多个则排序
		return this.mappedMethods.get(matches.get(0));
	}
	else {
		return null;
	}
}
```