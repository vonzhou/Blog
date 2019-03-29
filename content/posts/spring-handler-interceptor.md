---
title: "HandlerInterceptor应用及执行过程分析"
date: 2016-07-23
draft: false
categories: ["Spring"]
tags: [ "Spring", "Spring MVC"]
---

## HandlerInterceptor 实践

这两天花了很多时间在折腾使用AOP对Spring MVC Controller进行拦截，但是没有效果。然后尝试了下Spring的HandlerInterceptor，使用起来比较简单，思想也容易理解。下面是Spring Doc对HandlerInterceptor接口及相关方法的说明。

HandlerInterceptor 接口：

Workflow interface that allows for customized handler execution chains. Applications can register any number of existing or custom interceptors for certain groups of handlers, to add common pre-processing behavior without needing to modify each handler implementation.
A HandlerInterceptor gets called before the appropriate HandlerAdapter triggers the execution of the handler itself. This mechanism can be used for a large field of preprocessing aspects, e.g. for authorization checks, or common handler behavior like locale or theme changes. Its main purpose is to permit the factoring out of otherwise repetitive handler code.

Typically an interceptor chain is defined per HandlerMapping bean, sharing its granularity. To be able to apply a certain interceptor chain to a group of handlers, one needs to map the desired handlers via one HandlerMapping bean. The interceptors themselves are defined as beans in the application context, referenced by the mapping bean definition via its “interceptors” property (in XML: a of elements).

A HandlerInterceptor is basically similar to a Servlet Filter, but in contrast to the latter it allows custom pre-processing with the option to prohibit the execution of the handler itself, and custom post-processing. Filters are more powerful; for example they allow for exchanging the request and response objects that are handed down the chain. Note that a filter gets configured in web.xml, a HandlerInterceptor in the application context.

As a basic guideline, fine-grained handler-related pre-processing tasks are candidates for HandlerInterceptor implementations, especially factored-out common handler code and authorization checks. On the other hand, a Filter is well-suited for request content and view content handling, like multipart forms and GZIP compression. This typically shows when one needs to map the filter to certain content types (e.g. images), or to all requests.

preHandle 方法：

Intercept the execution of a handler. Called after HandlerMapping determined an appropriate handler object, but before HandlerAdapter invokes the handler.
DispatcherServlet processes a handler in an execution chain, consisting of any number of interceptors, with the handler itself at the end. With this method, each interceptor can decide to abort the execution chain, typically sending a HTTP error or writing a custom response.

postHandle 方法：

Intercept the execution of a handler. Called after HandlerAdapter actually invoked the handler, but before the DispatcherServlet renders the view. Can expose additional model objects to the view via the given ModelAndView.
DispatcherServlet processes a handler in an execution chain, consisting of any number of interceptors, with the handler itself at the end. With this method, each interceptor can post-process an execution, getting applied in inverse order of the execution chain.

afterCompletion 方法：

Callback after completion of request processing, that is, after rendering the view. Will be called on any outcome of handler execution, thus allows for proper resource cleanup.
Note: Will only be called if this interceptor’s preHandle method has successfully completed and returned true!
As with the postHandle method, the method will be invoked on each interceptor in the chain in reverse order, so the first interceptor will be the last to be invoked.


接下来是一个具体实例，[完整代码](https://github.com/vonzhou/SpringInAction3/tree/master/spring-interceptor)：

```java
public class LogInterceptor extends HandlerInterceptorAdapter {

    private static Logger logger = Logger.getLogger(LogInterceptor.class);

    //  Intercept the execution of a handler.
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,
                             Object handler) throws Exception {

        if(!isValidUser()){
            logger.info("Invalid user from " + request.getRemoteAddr());
            response.sendRedirect("http://localhost:8888/user/error");
            return false;
        }

        long startTime = System.currentTimeMillis();
        request.setAttribute("startTime", startTime);
        logger.info("Will call " + handler.toString());
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        logger.info("before return view  page, i can get model = " + modelAndView.getModelMap().get("hello"));
    }

    // Callback after completion of request processing, that is, after rendering the view.
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        // Our Log Func
        long curTime = System.currentTimeMillis();
        long startTime = (Long)request.getAttribute("startTime");
        long cost = curTime - startTime;
        logger.info("Call cost time " + cost + " mills!");
    }

    // FAKE
    private boolean isValidUser(){
        return true;
    }
}
```

application context中对拦截器的配置：

```xml
<mvc:interceptors>
        <mvc:interceptor>
            <mvc:mapping path="/**"/>
            <mvc:exclude-mapping path="/admin/**"/>
            <bean class="com.vonzhou.learning.interceptor.LogInterceptor"/>
        </mvc:interceptor>
    </mvc:interceptors>
```

所以当我们访问对应的URL时就会触发拦截器的执行，如下：

```bash
➜  ~ curl http://localhost:8888/user/service


You are our user, Welcome!
```
server端的日志输出：

```bash
2016-07-23 10:25:37,374  INFO LogInterceptor:32 - Will call public java.lang.String com.vonzhou.learning.controller.UserController.serveUser(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse,java.util.Locale,org.springframework.ui.ModelMap)
2016-07-23 10:25:38,379  INFO LogInterceptor:38 - before return view  page, i can get model = Some Data
2016-07-23 10:25:38,381  INFO LogInterceptor:50 - Call cost time 1007 mills!
```

## 执行过程分析

我们只看该逻辑相关的代码，其他的可以忽略掉，做到有目的的阅读源码。

### HttpServlet

Service层处理HTTP请求的入口是service()方法（更深层次的需要看Tomcat的原理），分别处理HTTP不同的方法，这里我们看GET方法的逻辑。

```java
public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
    HttpServletRequest request;
    HttpServletResponse response;
    try {
        request = (HttpServletRequest) req;
        response = (HttpServletResponse) res;
    } catch (ClassCastException e) {
        throw new ServletException("non-HTTP request or response");
    }
    service(request, response);
}

protected void service(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    String method = req.getMethod();

    if (method.equals(METHOD_GET)) {
        long lastModified = getLastModified(req);
        if (lastModified == -1) {
            // servlet doesn't support if-modified-since, no reason
            // to go through further expensive logic
            doGet(req, resp);
        } else {
            long ifModifiedSince = req.getDateHeader(HEADER_IFMODSINCE);
            if (ifModifiedSince < (lastModified / 1000 * 1000)) {
                // If the servlet mod time is later, call doGet()
                // Round down to the nearest second for a proper compare
                // A ifModifiedSince of -1 will always be less
                maybeSetLastModified(resp, lastModified);
                doGet(req, resp);
            } else {
                resp.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
            }
        }

    } else if (method.equals(METHOD_HEAD)) {
        long lastModified = getLastModified(req);
        maybeSetLastModified(resp, lastModified);
        doHead(req, resp);

    } else if (method.equals(METHOD_POST)) {
        doPost(req, resp);

    } else if (method.equals(METHOD_PUT)) {
        doPut(req, resp);

    } else if (method.equals(METHOD_DELETE)) {
        doDelete(req, resp);

    } else if (method.equals(METHOD_OPTIONS)) {
        doOptions(req, resp);

    } else if (method.equals(METHOD_TRACE)) {
        doTrace(req, resp);

    } else {
        //
        // Note that this means NO servlet supports whatever
        // method was requested, anywhere on this server.
        //

        String errMsg = lStrings.getString("http.method_not_implemented");
        Object[] errArgs = new Object[1];
        errArgs[0] = method;
        errMsg = MessageFormat.format(errMsg, errArgs);

        resp.sendError(HttpServletResponse.SC_NOT_IMPLEMENTED, errMsg);
    }
}
```

### FrameworkServlet

进入到Spring的框架逻辑中，调用doService，然后发布一个事件，这里重点看处理请求的doService方法，FrameworkServlet中该方法为abstract，具体在DispatcherServlet中实现。

```java
@Override
protected final void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {

    processRequest(request, response);
}

protected final void processRequest(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {

    long startTime = System.currentTimeMillis();
    Throwable failureCause = null;

    // Expose current LocaleResolver and request as LocaleContext.
    LocaleContext previousLocaleContext = LocaleContextHolder.getLocaleContext();
    LocaleContextHolder.setLocaleContext(buildLocaleContext(request), this.threadContextInheritable);

    // Expose current RequestAttributes to current thread.
    RequestAttributes previousRequestAttributes = RequestContextHolder.getRequestAttributes();
    ServletRequestAttributes requestAttributes = null;
    if (previousRequestAttributes == null || previousRequestAttributes.getClass().equals(ServletRequestAttributes.class)) {
        requestAttributes = new ServletRequestAttributes(request);
        RequestContextHolder.setRequestAttributes(requestAttributes, this.threadContextInheritable);
    }

    if (logger.isTraceEnabled()) {
        logger.trace("Bound request context to thread: " + request);
    }

    try {
        doService(request, response);
    } catch (ServletException ex) {
        failureCause = ex;
        throw ex;
    } catch (IOException ex) {
        failureCause = ex;
        throw ex;
    } catch (Throwable ex) {
        failureCause = ex;
        throw new NestedServletException("Request processing failed", ex);
    } finally {
        // Clear request attributes and reset thread-bound context.
        LocaleContextHolder.setLocaleContext(previousLocaleContext, this.threadContextInheritable);
        if (requestAttributes != null) {
            RequestContextHolder.setRequestAttributes(previousRequestAttributes, this.threadContextInheritable);
            requestAttributes.requestCompleted();
        }
        if (logger.isTraceEnabled()) {
            logger.trace("Cleared thread-bound request context: " + request);
        }

        if (failureCause != null) {
            this.logger.debug("Could not complete request", failureCause);
        } else {
            this.logger.debug("Successfully completed request");
        }
        if (this.publishEvents) {
            // Whether or not we succeeded, publish an event.
            long processingTime = System.currentTimeMillis() - startTime;
            this.webApplicationContext.publishEvent(
                    new ServletRequestHandledEvent(this,
                            request.getRequestURI(), request.getRemoteAddr(),
                            request.getMethod(), getServletConfig().getServletName(),
                            WebUtils.getSessionId(request), getUsernameForRequest(request),
                            processingTime, failureCause));
        }
    }
}
```
### DispatcherServlet

doDispatch中具体处理每个请求，包括Interceptor的拦截逻辑和Controller handler的业务逻辑。

```java
@Override
protected void doService(HttpServletRequest request, HttpServletResponse response) throws Exception {
    if (logger.isDebugEnabled()) {
        String requestUri = urlPathHelper.getRequestUri(request);
        logger.debug("DispatcherServlet with name '" + getServletName() + "' processing " + request.getMethod() +
                " request for [" + requestUri + "]");
    }

    /**
     * Make framework objects available to handlers and view objects.
     * 为了处理器对象，视图对象可以访问某些某些全局的对象，设置到HTTP request的属性中
     * */
    request.setAttribute(WEB_APPLICATION_CONTEXT_ATTRIBUTE, getWebApplicationContext());
    request.setAttribute(LOCALE_RESOLVER_ATTRIBUTE, this.localeResolver);
    request.setAttribute(THEME_RESOLVER_ATTRIBUTE, this.themeResolver);
    request.setAttribute(THEME_SOURCE_ATTRIBUTE, getThemeSource());

    try {
        doDispatch(request, response);
    } finally {
    }
}

/**
 * 具体分发请求到handler
 * <p>The handler will be obtained by applying the servlet's HandlerMappings in order.
 * The HandlerAdapter will be obtained by querying the servlet's installed HandlerAdapters
 * to find the first that supports the handler class.
 * <p>All HTTP methods are handled by this method. It's up to HandlerAdapters or handlers
 * themselves to decide which methods are acceptable.
 *
 * @param request  current HTTP request
 * @param response current HTTP response
 * @throws Exception in case of any kind of processing failure
 */
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
    HttpServletRequest processedRequest = request;
    HandlerExecutionChain mappedHandler = null;
    int interceptorIndex = -1;

    try {
        ModelAndView mv;
        boolean errorView = false;

        try {
            processedRequest = checkMultipart(request);

            /**
             * 获取该请求对应的 handler和interceptor（定位到了某个类）
             * Determine handler for the current request.
             * */
            mappedHandler = getHandler(processedRequest, false);
            if (mappedHandler == null || mappedHandler.getHandler() == null) {
                noHandlerFound(processedRequest, response);
                return;
            }

            /**
             * 获得该请求对应的更具体的handler（适配器模式，包含更多的策略和配置），如AnnotationMethodHandlerAdapter
             * Determine handler adapter for the current request.
             * */
            HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());

            /**
             * 依次执行我们的Interceptor
             * Apply preHandle methods of registered interceptors.
             * */
            HandlerInterceptor[] interceptors = mappedHandler.getInterceptors();
            if (interceptors != null) {
                for (int i = 0; i < interceptors.length; i++) {
                    HandlerInterceptor interceptor = interceptors[i];
                    if (!interceptor.preHandle(processedRequest, response, mappedHandler.getHandler())) {
                        /**
                         * 如果该preHandle方法返回了false，那么就倒序依次执行前面的Interceptor的 afterCompletion 方法，然后返回
                         * 所以不会执行后面的 Controller的handler方法，以及Interceptor的postHandle方法
                         * */
                        triggerAfterCompletion(mappedHandler, interceptorIndex, processedRequest, response, null);
                        return;
                    }
                    interceptorIndex = i;
                }
            }

            /**
             * 真正进入 Controller handler 进行请求处理
             * Actually invoke the handler.
             * */
            mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

            // Do we need view name translation?
            if (mv != null && !mv.hasView()) {
                mv.setViewName(getDefaultViewName(request));
            }

            //
            /**
             * 然后逆序依次执行我们的Interceptor的 postHandle 方法
             * Apply postHandle methods of registered interceptors.
             * */
            if (interceptors != null) {
                for (int i = interceptors.length - 1; i >= 0; i--) {
                    HandlerInterceptor interceptor = interceptors[i];
                    interceptor.postHandle(processedRequest, response, mappedHandler.getHandler(), mv);
                }
            }
        } catch (ModelAndViewDefiningException ex) {
            logger.debug("ModelAndViewDefiningException encountered", ex);
            mv = ex.getModelAndView();
        } catch (Exception ex) {
            Object handler = (mappedHandler != null ? mappedHandler.getHandler() : null);
            mv = processHandlerException(processedRequest, response, handler, ex);
            errorView = (mv != null);
        }

        // Did the handler return a view to render?
        if (mv != null && !mv.wasCleared()) {
            render(mv, processedRequest, response);
            if (errorView) {
                WebUtils.clearErrorRequestAttributes(request);
            }
        } else {
            if (logger.isDebugEnabled()) {
                logger.debug("Null ModelAndView returned to DispatcherServlet with name '" + getServletName() +
                        "': assuming HandlerAdapter completed request handling");
            }
        }

        /** 此时所有的Interceptor都顺利完成了（preHandle -> handler -> postHandle），
         * 此时倒序依次执行所有的Interceptor的 afterCompletion方法
         * Trigger after-completion for successful outcome.
         * */
        triggerAfterCompletion(mappedHandler, interceptorIndex, processedRequest, response, null);
    } catch (Exception ex) {
        // Trigger after-completion for thrown exception.
        triggerAfterCompletion(mappedHandler, interceptorIndex, processedRequest, response, ex);
        throw ex;
    } catch (Error err) {
        ServletException ex = new NestedServletException("Handler processing failed", err);
        // Trigger after-completion for thrown exception.
        triggerAfterCompletion(mappedHandler, interceptorIndex, processedRequest, response, ex);
        throw ex;
    } finally {
        // Clean up any resources used by a multipart request.
        if (processedRequest != request) {
            cleanupMultipart(processedRequest);
        }
    }
}

private void triggerAfterCompletion(HandlerExecutionChain mappedHandler,
                                    int interceptorIndex,
                                    HttpServletRequest request,
                                    HttpServletResponse response,
                                    Exception ex) throws Exception {

    // Apply afterCompletion methods of registered interceptors.
    if (mappedHandler != null) {
        HandlerInterceptor[] interceptors = mappedHandler.getInterceptors();
        if (interceptors != null) {
            for (int i = interceptorIndex; i >= 0; i--) {
                HandlerInterceptor interceptor = interceptors[i];
                try {
                    interceptor.afterCompletion(request, response, mappedHandler.getHandler(), ex);
                } catch (Throwable ex2) {
                    logger.error("HandlerInterceptor.afterCompletion threw exception", ex2);
                }
            }
        }
    }
}
```

## 总结

![流程图](/images/spring-handler-interceptor-1.jpg)
