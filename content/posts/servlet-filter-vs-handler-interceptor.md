---
title: "Servlet Filter与HandlerInterceptor的对比"
date: 2016-11-13
draft: false
categories: ["Spring"]
tags: [ "Spring", "Spring MVC", "Servlet"]
---



## 前言

好久么有写博客了，这是之前总结的一篇。

对于Servlet Filter，官方文档中说的很好， 并且给出了常见的应用场景。

A filter is an object that performs filtering tasks on either the request to a resource (a servlet or static content), or on the response from a resource, or both. Filters perform filtering in the doFilter method. Every Filter has access to a FilterConfig object from which it can obtain its initialization parameters, and a reference to the ServletContext which it can use, for example, to load resources needed for filtering tasks.

Filters are configured in the deployment descriptor of a web application.

Examples that have been identified for this design are:

* Authentication Filters
* Logging and Auditing Filters
* Image conversion Filters
* Data compression Filters
* Encryption Filters
* Tokenizing Filters
* Filters that trigger resource access events
* XSL/T filters
* Mime-type chain Filter

接下来用简单的例子进行理解。

## 示例

实现Filter接口。

```java
public class SimpleServletFilter implements Filter{
    private static Logger logger = Logger.getLogger(SimpleServletFilter.class);

    public void init(FilterConfig filterConfig) throws ServletException {
        logger.info("SimpleServletFilter init....");
    }

    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        String id = request.getParameter("id");
        if(id != null && !id.isEmpty() && !id.equals("123")){
            chain.doFilter(request,response);
        }

        // Reply directly here
        HttpServletResponse httpResponse = (HttpServletResponse)response;
        httpResponse.getWriter().print("Another Page...enjoy");
    }

    public void destroy() {
        logger.info("SimpleServletFilter destroy....");
    }
}
```

配置部署文件, filter所有的请求（？有问题，后面会说）。

```xml
<filter>
        <filter-name>simpleFilter</filter-name>
        <filter-class>com.vonzhou.learning.filter.SimpleServletFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>simpleFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
```
通过运行日志输出，结合前文《HandlerInterceptor应用及执行过程分析》的对比,可以很清楚的看出filter和interceptor大概的生命周期。filter比interceptor更早出生，更晚死去。

```bash
2016-07-23 14:07:18,581  INFO SimpleServletFilter:16 - SimpleServletFilter init....
[2016-07-23 02:07:18,965] Artifact spring-interceptor:war exploded: Artifact is deployed successfully
[2016-07-23 02:07:18,965] Artifact spring-interceptor:war exploded: Deploy took 5,416 milliseconds
2016-07-23 14:07:24,133  INFO LogInterceptor:32 - Will call public java.lang.String com.vonzhou.learning.controller.UserController.serveUser(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse,java.util.Locale,org.springframework.ui.ModelMap)
2016-07-23 14:07:25,164  INFO LogInterceptor:38 - before return view  page, i can get model = Some Data
2016-07-23 14:07:25,848  INFO LogInterceptor:48 - Call cost time 1715 mills!
2016-07-23 14:07:28,389  INFO LogInterceptor:32 - Will call public java.lang.String com.vonzhou.learning.controller.UserController.serveUser(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse,java.util.Locale,org.springframework.ui.ModelMap)
2016-07-23 14:07:29,393  INFO LogInterceptor:38 - before return view  page, i can get model = Some Data
2016-07-23 14:07:29,395  INFO LogInterceptor:48 - Call cost time 1006 mills!
/usr/local/apache-tomcat-8.0.33/bin/catalina.sh stop
2016-07-23 14:08:12,607  INFO SimpleServletFilter:31 - SimpleServletFilter destroy....
Disconnected from server
```

[完整代码](https://github.com/vonzhou/SpringInAction3/tree/master/spring-interceptor)

## 对比总结

* filter是比interceptor强大
* filter操纵request，response的能力更大，可以直接response回应客户端，【×但是在interceptor的preHandle方法中操纵response不起作用】都可以
* filter的粒度是更靠近前端的request级别，而interceptor处理的粒度测试靠近后端的Controller（或称为handler）的被映射的请求处理方法
* filter可以双向的，根据request或者response来响应，但是interceptor只能是拦截进入这一端
* 过程中发现，如果对静态资源配置了`<mvc:resources mapping="/resources/**" location="/resources/"/>`，那么如果访问的静态资源文件存在的话，filter并不会起作用（web.xml中的filter配置如下）,即使把url-pattern指定为`<url-pattern>/resources/*</url-pattern>`（其实/*就匹配了所有的请求）。说明了mvc:resources配置的静态文件并不会经过Servlet filter， 虽然说filter很强大。

```xml
<filter>
    <filter-name>simpleFilter</filter-name>
    <filter-class>com.vonzhou.learning.filter.SimpleServletFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>simpleFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

前面我说在interceptor的preHandle方法中操纵response不起作用，其实不够全面, 比如在preHandle方法中设置断点，当response回复消息后，此时shutdown服务器，这时在客户端会收到这里的消息。 在interceptor中如果要直接响应HTTP，也是可以的，但是要return false，中断后续的处理逻辑。
```java
response.getWriter().println(" --- From Interceptor, you are rejected.");
response.flushBuffer();

return false;
```

【×另一种情况就更加奇怪，如果在interceptor中的 preHandle 方法中 response write消息之后是 return false，此时返回的消息同时包含了filter中被拦截成功后应该返回的消息（见下面），所以这时就崩溃了，一片混乱，所以只能在使用 handlerinterceptor 的时候不要使用response回复消息了。】 这里是自己理解错误！

关键点看自己在filter中实现怎样的逻辑，你可以只是filter请求的入口，像这样：

```java
if (meetFilterCondition(request)) {
    chain.doFilter(request, response);
} else {
    // Reply directly here
    replyDirectly(response);
}
```

也可以在请求入口和响应的出口都做一些filter处理，像这样：

```java
if (meetFilterCondition(request)) {
    chain.doFilter(request, response);
} else {
    // Reply directly here (1)
    replyDirectly(response);
}

// filter outside  (2)
doFilterResponse(response);
```

