---
title: "解决Zuul无法同时转发Multipart和JSON请求的问题"
date: 2018-10-10
draft: false
categories: ["SpringCloud"]
tags: ["SpringBoot", "Zuul", "JSON"]
---

扩展 RibbonRoutingFilter，修改默认的转发逻辑，支持转发Multipart和JSON类型请求。

## 场景

系统中有一个采用 Netflix Zuul 实现的网关模块，负责统一的鉴权，然后把请求转到对应的后端模块。基本的配置后，只需要实现一个Filter就可以了。

```java
@Slf4j
@Component
public class AccessTokenFilter extends ZuulFilter {

	// Filter 的类型，在路由之前
    @Override
    public String filterType() {
        return "pre";
    }

	// 比系统的优先级要低些
    @Override
    public int filterOrder() {
        return 7;
    }


    @Override
    public Object run() {
        RequestContext requestContext = RequestContext.getCurrentContext();
        HttpServletRequest request = requestContext.getRequest();
        HttpServletResponse response = requestContext.getResponse();

        
        String token = CookieUtils.getCookieValue("token", request);
        log.info("token={}", token);

        token = URLDecoder.decode(token, "UTF-8");
		// 验证 token
		boolean valid = validateToken(token);

		// 验证不通过则直接响应
		if(!valid){
			 setFalseZuulResponse(requestContext);
		}

        return null;
    }

    /**
     * 不再路由，直接响应.
     */
    private void setFalseZuulResponse(RequestContext requestContext) {
        requestContext.setSendZuulResponse(false); 
        requestContext.setResponseBody("error");
    }
}
```

一切都OK，可是有一天出现了问题。

## 环境

Spring Boot 版本：

```java
<parent>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-parent</artifactId>
<version>1.4.2.RELEASE</version>
<relativePath/> <!-- lookup parent from repository -->
</parent>
```

Spring Cloud 版本：


```java
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-dependencies</artifactId>
    <version>Brixton.SR5</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```


## 问题背景

有一天，新增了一个接口，URL中带有JSON串，发现访问该接口时请求无法到达后端。网关模块抛出了异常 URISyntaxException。

```java
Caused by: java.net.URISyntaxException: Illegal character in query at index 65: http://10.201.169.146:8091/api/.../?param=%7B"a":"","b":"","c":""%7D
	at java.net.URI$Parser.fail(URI.java:2848)
	at java.net.URI$Parser.checkChars(URI.java:3021)
	at java.net.URI$Parser.parseHierarchical(URI.java:3111)
	at java.net.URI$Parser.parse(URI.java:3053)
	at java.net.URI.<init>(URI.java:588)
	at com.sun.jersey.api.uri.UriBuilderImpl.createURI(UriBuilderImpl.java:721)
```

很慌，然后Goolge后发现这个问题[别人也遇到过](https://github.com/spring-cloud/spring-cloud-netflix/issues/918)，说这个版本的Zuul默认使用的是 Ribbon Client，换成 http client 就可以了。


```java
@Bean
public RibbonCommandFactory<?> ribbonCommandFactory(
        final SpringClientFactory clientFactory) {
    return new HttpClientRibbonCommandFactory(clientFactory);
}
```

的确解决了这个问题，但是又出现了新的问题：之前的 Multipart/form-data POST 请求转发到后端服务器后出现了 ` java.io.IOException: Incomplete parts`。


```java
2018-10-09 19:04:22.591  WARN 12137 --- [qtp289592183-19] o.e.jetty.server.handler.ErrorHandler    : EXCEPTION 

org.springframework.web.util.NestedServletException: Request processing failed; nested exception is org.springframework.web.multipart.MultipartException: Could not parse multipart servlet request; nested exception is java.io.IOException: Incomplete parts
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:982)
	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:872)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:846)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:790)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:845)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:584)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:143)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:566)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:226)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1180)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:512)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:185)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1112)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:141)
	at org.eclipse.jetty.server.Dispatcher.forward(Dispatcher.java:199)
	at org.eclipse.jetty.server.Dispatcher.error(Dispatcher.java:79)
	at org.eclipse.jetty.server.handler.ErrorHandler.handle(ErrorHandler.java:94)
	at org.springframework.boot.context.embedded.jetty.JettyEmbeddedErrorHandler.handle(JettyEmbeddedErrorHandler.java:55)
	at org.eclipse.jetty.server.Response.sendError(Response.java:558)
	at org.eclipse.jetty.server.Response.sendError(Response.java:497)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:651)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:143)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:548)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:226)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1180)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:512)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:185)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1112)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:141)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:134)
	at org.eclipse.jetty.server.Server.handle(Server.java:534)
	at org.eclipse.jetty.server.HttpChannel.handle(HttpChannel.java:320)
	at org.eclipse.jetty.server.HttpConnection.onFillable(HttpConnection.java:251)
	at org.eclipse.jetty.io.AbstractConnection$ReadCallback.succeeded(AbstractConnection.java:273)
	at org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:95)
	at org.eclipse.jetty.io.SelectChannelEndPoint$2.run(SelectChannelEndPoint.java:93)
	at org.eclipse.jetty.util.thread.strategy.ExecuteProduceConsume.executeProduceConsume(ExecuteProduceConsume.java:303)
	at org.eclipse.jetty.util.thread.strategy.ExecuteProduceConsume.produceConsume(ExecuteProduceConsume.java:148)
	at org.eclipse.jetty.util.thread.strategy.ExecuteProduceConsume.run(ExecuteProduceConsume.java:136)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:671)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$2.run(QueuedThreadPool.java:589)
	at java.lang.Thread.run(Thread.java:745)
Caused by: org.springframework.web.multipart.MultipartException: Could not parse multipart servlet request; nested exception is java.io.IOException: Incomplete parts
	at org.springframework.web.multipart.support.StandardMultipartHttpServletRequest.parseRequest(StandardMultipartHttpServletRequest.java:111)
	at org.springframework.web.multipart.support.StandardMultipartHttpServletRequest.<init>(StandardMultipartHttpServletRequest.java:85)
	at org.springframework.web.multipart.support.StandardServletMultipartResolver.resolveMultipart(StandardServletMultipartResolver.java:76)
	at org.springframework.web.servlet.DispatcherServlet.checkMultipart(DispatcherServlet.java:1099)
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:932)
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:897)
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:970)
	... 42 common frames omitted
Caused by: java.io.IOException: Incomplete parts
	at org.eclipse.jetty.util.MultiPartInputStreamParser.parse(MultiPartInputStreamParser.java:781)
	at org.eclipse.jetty.util.MultiPartInputStreamParser.getParts(MultiPartInputStreamParser.java:422)
	at org.eclipse.jetty.server.Request.getParts(Request.java:2317)
	at org.eclipse.jetty.server.Request.extractMultipartParameters(Request.java:519)
	at org.eclipse.jetty.server.Request.extractContentParameters(Request.java:441)
	at org.eclipse.jetty.server.Request.getParameters(Request.java:365)
	at org.eclipse.jetty.server.Request.getParameter(Request.java:996)
	at org.springframework.web.filter.HiddenHttpMethodFilter.doFilterInternal(HiddenHttpMethodFilter.java:70)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107)
	at org.eclipse.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1699)
	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:197)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107)
	at org.eclipse.jetty.servlet.ServletHandler$CachedChain.doFilter(ServletHandler.java:1699)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:582)
	... 21 common frames omitted
```

异常抛的位置是 `org.eclipse.jetty.util.MultiPartInputStreamParser#parse`：

```java
// 草，这么长
protected void parse ()
{
    //have we already parsed the input?
    if (_parts != null || _err != null)
        return;

    //initialize
    long total = 0; //keep running total of size of bytes read from input and throw an exception if exceeds MultipartConfigElement._maxRequestSize
    _parts = new MultiMap<>();

    //if its not a multipart request, don't parse it
    if (_contentType == null || !_contentType.startsWith("multipart/form-data"))
        return;

    try
    {
        //sort out the location to which to write the files

        if (_config.getLocation() == null)
            _tmpDir = _contextTmpDir;
        else if ("".equals(_config.getLocation()))
            _tmpDir = _contextTmpDir;
        else
        {
            File f = new File (_config.getLocation());
            if (f.isAbsolute())
                _tmpDir = f;
            else
                _tmpDir = new File (_contextTmpDir, _config.getLocation());
        }

        if (!_tmpDir.exists())
            _tmpDir.mkdirs();

        String contentTypeBoundary = "";
        int bstart = _contentType.indexOf("boundary=");
        if (bstart >= 0)
        {
            int bend = _contentType.indexOf(";", bstart);
            bend = (bend < 0? _contentType.length(): bend);
            contentTypeBoundary = QuotedStringTokenizer.unquote(value(_contentType.substring(bstart,bend)).trim());
        }

        String boundary="--"+contentTypeBoundary;
        String lastBoundary=boundary+"--";
        byte[] byteBoundary=lastBoundary.getBytes(StandardCharsets.ISO_8859_1);

        // Get first boundary
        String line = null;
        try
        {
            line=((ReadLineInputStream)_in).readLine();
        }
        catch (IOException e)
        {
            LOG.warn("Badly formatted multipart request");
            throw e;
        }

        if (line == null)
            throw new IOException("Missing content for multipart request");

        boolean badFormatLogged = false;
        line=line.trim();
        while (line != null && !line.equals(boundary) && !line.equals(lastBoundary))
        {
            if (!badFormatLogged)
            {
                LOG.warn("Badly formatted multipart request");
                badFormatLogged = true;
            }
            line=((ReadLineInputStream)_in).readLine();
            line=(line==null?line:line.trim());
        }

        if (line == null)
            throw new IOException("Missing initial multi part boundary");

        // Empty multipart.
        if (line.equals(lastBoundary))
            return;

        // 开始解析 Multipart
        // Read each part
        boolean lastPart=false;

        outer:while(!lastPart)
        {
            String contentDisposition=null;
            String contentType=null;
            String contentTransferEncoding=null;

            MultiMap<String> headers = new MultiMap<>();
            while(true)
            {
                line=((ReadLineInputStream)_in).readLine();

                //No more input
                if(line==null)
                    break outer;

                //end of headers:
                if("".equals(line))
                    break;

                total += line.length();
                if (_config.getMaxRequestSize() > 0 && total > _config.getMaxRequestSize())
                    throw new IllegalStateException ("Request exceeds maxRequestSize ("+_config.getMaxRequestSize()+")");

                //get content-disposition and content-type
                int c=line.indexOf(':',0);
                if(c>0)
                {
                    String key=line.substring(0,c).trim().toLowerCase(Locale.ENGLISH);
                    String value=line.substring(c+1,line.length()).trim();
                    headers.put(key, value);
                    if (key.equalsIgnoreCase("content-disposition"))
                        contentDisposition=value;
                    if (key.equalsIgnoreCase("content-type"))
                        contentType = value;
                    if(key.equals("content-transfer-encoding"))
                        contentTransferEncoding=value;
                }
            }

            // Extract content-disposition
            boolean form_data=false;
            if(contentDisposition==null)
            {
                throw new IOException("Missing content-disposition");
            }

            QuotedStringTokenizer tok=new QuotedStringTokenizer(contentDisposition,";", false, true);
            String name=null;
            String filename=null;
            while(tok.hasMoreTokens())
            {
                String t=tok.nextToken().trim();
                String tl=t.toLowerCase(Locale.ENGLISH);
                if(t.startsWith("form-data"))
                    form_data=true;
                else if(tl.startsWith("name="))
                    name=value(t);
                else if(tl.startsWith("filename="))
                    filename=filenameValue(t);
            }

            // Check disposition
            if(!form_data)
            {
                continue;
            }
            //It is valid for reset and submit buttons to have an empty name.
            //If no name is supplied, the browser skips sending the info for that field.
            //However, if you supply the empty string as the name, the browser sends the
            //field, with name as the empty string. So, only continue this loop if we
            //have not yet seen a name field.
            if(name==null)
            {
                continue;
            }

            //Have a new Part
            MultiPart part = new MultiPart(name, filename);
            part.setHeaders(headers);
            part.setContentType(contentType);
            _parts.add(name, part);
            part.open();

            InputStream partInput = null;
            if ("base64".equalsIgnoreCase(contentTransferEncoding))
            {
                partInput = new Base64InputStream((ReadLineInputStream)_in);
            }
            else if ("quoted-printable".equalsIgnoreCase(contentTransferEncoding))
            {
                partInput = new FilterInputStream(_in)
                {
                    @Override
                    public int read() throws IOException
                    {
                        int c = in.read();
                        if (c >= 0 && c == '=')
                        {
                            int hi = in.read();
                            int lo = in.read();
                            if (hi < 0 || lo < 0)
                            {
                                throw new IOException("Unexpected end to quoted-printable byte");
                            }
                            char[] chars = new char[] { (char)hi, (char)lo };
                            c = Integer.parseInt(new String(chars),16);
                        }
                        return c;
                    }
                };
            }
            else
                partInput = _in;


            try
            {
                int state=-2;
                int c;
                boolean cr=false;
                boolean lf=false;

                // loop for all lines
                while(true)
                {
                    int b=0;
                    while((c=(state!=-2)?state:partInput.read())!=-1)
                    {
                        total ++;
                        if (_config.getMaxRequestSize() > 0 && total > _config.getMaxRequestSize())
                            throw new IllegalStateException("Request exceeds maxRequestSize ("+_config.getMaxRequestSize()+")");

                        state=-2;

                        // look for CR and/or LF
                        if(c==13||c==10)
                        {
                            if(c==13)
                            {
                                partInput.mark(1);
                                int tmp=partInput.read();
                                if (tmp!=10)
                                    partInput.reset();
                                else
                                    state=tmp;
                            }
                            break;
                        }

                        // Look for boundary
                        if(b>=0&&b<byteBoundary.length&&c==byteBoundary[b])
                        {
                            b++;
                        }
                        else
                        {
                            // Got a character not part of the boundary, so we don't have the boundary marker.
                            // Write out as many chars as we matched, then the char we're looking at.
                            if(cr)
                                part.write(13);

                            if(lf)
                                part.write(10);

                            cr=lf=false;
                            if(b>0)
                                part.write(byteBoundary,0,b);

                            b=-1;
                            part.write(c);
                        }
                    }

                    // Check for incomplete boundary match, writing out the chars we matched along the way
                    if((b>0&&b<byteBoundary.length-2)||(b==byteBoundary.length-1))
                    {
                        if(cr)
                            part.write(13);

                        if(lf)
                            part.write(10);

                        cr=lf=false;
                        part.write(byteBoundary,0,b);
                        b=-1;
                    }

                    // Boundary match. If we've run out of input or we matched the entire final boundary marker, then this is the last part.
                    if(b>0||c==-1)
                    {

                        if(b==byteBoundary.length)
                            lastPart=true;
                        if(state==10)
                            state=-2;
                        break;
                    }

                    // handle CR LF
                    if(cr)
                        part.write(13);

                    if(lf)
                        part.write(10);

                    cr=(c==13);
                    lf=(c==10||state==10);
                    if(state==10)
                        state=-2;
                }
            }
            finally
            {
                part.close();
            }
        }
        if (lastPart)
        {
            while(line!=null)
                line=((ReadLineInputStream)_in).readLine();
        }
        // 这里抛出的异常， 为何没有解析到所有的 part ？？？
        else
            throw new IOException("Incomplete parts");
    }
    catch (Exception e)
    {
        _err = e;
    }
}
```

最终没能定位到问题的根本原因。但是问题基本比较清晰了：使用默认的 RibbonCommandFactory（即RestClientRibbonCommandFactory） 可以处理 multipart/form 的请求，但是无法处理URL中含JSON的情况，而如果使用 HttpClientRibbonCommandFactory 则可以处理RUL中含JSON的情况，但是无法正确转发 multipart 的请求。

![RibbonCommandFactory类图](/images/zuul-forward-multipart-and-json.png)

问题出在路由转发的时候，后来想到能不能换一种思路：自己修改路由转发的逻辑根据请求的类型来指定使用不同的 RibbonCommandFactory？

## 解决方法

禁掉默认的路由过滤器 RibbonRoutingFilter。

```java
zuul.RibbonRoutingFilter.route.disable: true
```

然后扩展 RibbonRoutingFilter，修改默认的转发逻辑。

```java
@Slf4j
public class MyRibbonRoutingFilter extends RibbonRoutingFilter {

    @Autowired
    private RestClientRibbonCommandFactory restClientRibbonCommandFactory;

    @Autowired
    private HttpClientRibbonCommandFactory httpClientRibbonCommandFactory;

    public MyRibbonRoutingFilter(ProxyRequestHelper helper, RibbonCommandFactory<?> ribbonCommandFactory) {
        super(helper, ribbonCommandFactory);
    }

    public MyRibbonRoutingFilter(RibbonCommandFactory<?> ribbonCommandFactory) {
        super(ribbonCommandFactory);
    }


    protected ClientHttpResponse forward(RibbonCommandContext context) throws Exception {
        log.info("-------MyRibbonRoutingFilter forward--------");
        Map<String, Object> info = this.helper.debug(context.getVerb(), context.getUri(),
                context.getHeaders(), context.getParams(), context.getRequestEntity());

        RibbonCommandFactory rcf = this.restClientRibbonCommandFactory;

        if (!isMultipartForm()) {
            log.info("Not multipart/form request use HttpClientRibbonCommandFactory to handle url with json");
            rcf = httpClientRibbonCommandFactory;
        } else {
            log.info("Multipart/form request use default");
        }
        log.info("RibbonCommandFactory is " + rcf.getClass().getCanonicalName());

        RibbonCommand command = rcf.create(context);
        try {
            ClientHttpResponse response = command.execute();
            this.helper.appendDebug(info, response.getStatusCode().value(),
                    response.getHeaders());
            return response;
        } catch (HystrixRuntimeException ex) {
            return handleException(info, ex);
        }

    }

    private static boolean isMultipartForm() {
        RequestContext ctx = RequestContext.getCurrentContext();
        HttpServletRequest request = ctx.getRequest();
        String contentType = request.getContentType();
        if (contentType == null) {
            return false;
        }

        try {
            MediaType mediaType = MediaType.valueOf(contentType);
            return MediaType.MULTIPART_FORM_DATA.includes(mediaType);
        } catch (InvalidMediaTypeException ex) {
            return false;
        }
    }
}
```

当然这里的两个 RibbonCommandFactory bean 需要配置。

```java
@Configuration
public class RibbonCommandFactoryConfig {

    @Bean
    public HttpClientRibbonCommandFactory ribbonCommandFactory(final SpringClientFactory clientFactory) {
        return new HttpClientRibbonCommandFactory(clientFactory);
    }

    @Bean
    public RestClientRibbonCommandFactory ribbonCommandFactory2(final SpringClientFactory clientFactory) {
        return new RestClientRibbonCommandFactory(clientFactory);
    }
}
```

问题解决了，可以看到 Zuul 的扩展性挺好的。


