---
title: "jetty/tomcat容器在使用RequestParam注解处理PUT方法时的差异"
date: 2017-07-06
draft: false
categories: ["Spring"]
tags: [ "Spring", "Spring MVC", "Tomcat", "Jetty", "HTTP", "PUT"]
---


![执行流程](/images/tomcat-vs-jetty-put.jpg)


## 场景

Spring boot项目使用内嵌的server，有如下的一个Controller方法。

```java
@RestController
@RequestMapping("/hello")
public class HelloController {

    @PutMapping("/bind")
    public String test(@RequestParam String param) {
        return param;
    }

}
```

但是在使用jetty或tomcat时对于form-data，x-www-form-urlencoded格式的请求时表现的行为出现了差异：

* 内嵌jetty表现出来的兼容性最好，不论PUT，POST方法，不论请求体的格式form-data，x-www-form-urlencoded，注解RequestParam都能成功解析到参数param的值
* 内嵌tomcat有点问题，POST方法对于两种格式都支持，PUT方法对于form-data会抛出"the request param xx is not present"，对于x-www-form-urlencoded是OK的

无意间遇到的一个问题，折腾了几个小时，通过debug源码可以了解到，在spring层面上逻辑是比较清晰的，Spring中Multipart只支持POST方法，通过下面的方法可以看出(org.springframework.web.multipart.support.StandardServletMultipartResolver#isMultipart)
。


```java
public boolean isMultipart(HttpServletRequest request) {
	// Same check as in Commons FileUpload...
	if (!"post".equals(request.getMethod().toLowerCase())) {
		return false;
	}
	String contentType = request.getContentType();
	return (contentType != null && contentType.toLowerCase().startsWith("multipart/"));
}
```

在调用我们的handler之前都会从具体request中解析参数（org.springframework.web.method.annotation.RequestParamMethodArgumentResolver#resolveName）。



```java
protected Object resolveName(String name, MethodParameter parameter, NativeWebRequest request) throws Exception {
	HttpServletRequest servletRequest = request.getNativeRequest(HttpServletRequest.class);
	// PUT方法都无法解析为 MultipartRequest，这里为null
	MultipartHttpServletRequest multipartRequest =
			WebUtils.getNativeRequest(servletRequest, MultipartHttpServletRequest.class);

	Object mpArg = MultipartResolutionDelegate.resolveMultipartArgument(name, parameter, servletRequest);
	if (mpArg != MultipartResolutionDelegate.UNRESOLVABLE) {
		return mpArg;
	}

	Object arg = null;
	if (multipartRequest != null) {
		List<MultipartFile> files = multipartRequest.getFiles(name);
		if (!files.isEmpty()) {
			arg = (files.size() == 1 ? files.get(0) : files);
		}
	}
	// 所以参数从这里解析
	if (arg == null) {
		String[] paramValues = request.getParameterValues(name);
		if (paramValues != null) {
			arg = (paramValues.length == 1 ? paramValues[0] : paramValues);
		}
	}
	return arg;
}
```

至于具体的Request是什么，取决于server容器，虽然都实现了类似的规范。


## tomcat请求参数解析过程

解析参数过程：
org.apache.catalina.connector.Request#parseParameters


```java
protected void parseParameters() {

    parametersParsed = true;

    // 这里得到的参数为空
    Parameters parameters = coyoteRequest.getParameters();
    boolean success = false;
    try {
        // Set this every time in case limit has been changed via JMX
        parameters.setLimit(getConnector().getMaxParameterCount());

        // getCharacterEncoding() may have been overridden to search for
        // hidden form field containing request encoding
        String enc = getCharacterEncoding();

        boolean useBodyEncodingForURI = connector.getUseBodyEncodingForURI();
        if (enc != null) {
            parameters.setEncoding(enc);
            if (useBodyEncodingForURI) {
                parameters.setQueryStringEncoding(enc);
            }
        } else {
            parameters.setEncoding
                (org.apache.coyote.Constants.DEFAULT_CHARACTER_ENCODING);
            if (useBodyEncodingForURI) {
                parameters.setQueryStringEncoding
                    (org.apache.coyote.Constants.DEFAULT_CHARACTER_ENCODING);
            }
        }

        parameters.handleQueryParameters();

        if (usingInputStream || usingReader) {
            success = true;
            return;
        }
        
        if( !getConnector().isParseBodyMethod(getMethod()) ) {
            success = true;// PUT方法，不会解析body，直接返回
            return;
        }

        // 如果是POST方法，会执行这里，获取contentType：multipart/form-data或者applicatoin/x-www-form-urlencoded
        String contentType = getContentType();
        if (contentType == null) {
            contentType = "";
        }
        int semicolon = contentType.indexOf(';');
        if (semicolon >= 0) {
            contentType = contentType.substring(0, semicolon).trim();
        } else {
            contentType = contentType.trim();
        }

        if ("multipart/form-data".equals(contentType)) {
            parseParts(false); // 解析body part
            success = true;
            return;
        }

        if (!("application/x-www-form-urlencoded".equals(contentType))) {
            success = true;
            return;
        }

        // applicatoin/x-www-form-urlencoded格式会到这里
        int len = getContentLength();

        if (len > 0) {
            int maxPostSize = connector.getMaxPostSize();
            if ((maxPostSize >= 0) && (len > maxPostSize)) {
                Context context = getContext();
                if (context != null && context.getLogger().isDebugEnabled()) {
                    context.getLogger().debug(
                            sm.getString("coyoteRequest.postTooLarge"));
                }
                checkSwallowInput();
                parameters.setParseFailedReason(FailReason.POST_TOO_LARGE);
                return;
            }
            byte[] formData = null;
            if (len < CACHED_POST_LEN) {
                if (postData == null) {
                    postData = new byte[CACHED_POST_LEN];
                }
                formData = postData;
            } else {
                formData = new byte[len];
            }
            try {
                if (readPostBody(formData, len) != len) {
                    parameters.setParseFailedReason(FailReason.REQUEST_BODY_INCOMPLETE);
                    return;
                }
            } catch (IOException e) {
                // Client disconnect
                Context context = getContext();
                if (context != null && context.getLogger().isDebugEnabled()) {
                    context.getLogger().debug(
                            sm.getString("coyoteRequest.parseParameters"),
                            e);
                }
                parameters.setParseFailedReason(FailReason.CLIENT_DISCONNECT);
                return;
            }
            // 解析参数
            parameters.processParameters(formData, 0, len);
        } else if ("chunked".equalsIgnoreCase(
                coyoteRequest.getHeader("transfer-encoding"))) {
            byte[] formData = null;
            try {
                formData = readChunkedPostBody();
            } catch (IllegalStateException ise) {
                // chunkedPostTooLarge error
                parameters.setParseFailedReason(FailReason.POST_TOO_LARGE);
                Context context = getContext();
                if (context != null && context.getLogger().isDebugEnabled()) {
                    context.getLogger().debug(
                            sm.getString("coyoteRequest.parseParameters"),
                            ise);
                }
                return;
            } catch (IOException e) {
                // Client disconnect
                parameters.setParseFailedReason(FailReason.CLIENT_DISCONNECT);
                Context context = getContext();
                if (context != null && context.getLogger().isDebugEnabled()) {
                    context.getLogger().debug(
                            sm.getString("coyoteRequest.parseParameters"),
                            e);
                }
                return;
            }
            if (formData != null) {
                parameters.processParameters(formData, 0, formData.length);
            }
        }
        success = true;
    } finally {
        if (!success) {
            parameters.setParseFailedReason(FailReason.UNKNOWN);
        }
    }

}
```

## jetty请求参数解析过程

org.eclipse.jetty.server.Request#getParameterValues

```java
public String[] getParameterValues(String name)
{
    List<String> vals = getParameters().getValues(name);
    if (vals == null)
        return null;
    return vals.toArray(new String[vals.size()]);
}

private MultiMap<String> getParameters()
{
    if (!_contentParamsExtracted) 
    {
        // content parameters need boolean protection as they can only be read
        // once, but may be reset to null by a reset
        _contentParamsExtracted = true;

        // Extract content parameters; these cannot be replaced by a forward()
        // once extracted and may have already been extracted by getParts() or
        // by a processing happening after a form-based authentication.
        if (_contentParameters == null)
            extractContentParameters();
    }
    
    // Extract query string parameters; these may be replaced by a forward()
    // and may have already been extracted by mergeQueryParameters().
    if (_queryParameters == null)
        extractQueryParameters();

    // Do parameters need to be combined?
    if (_queryParameters==NO_PARAMS || _queryParameters.size()==0)
        _parameters=_contentParameters; // 这里
    else if (_contentParameters==NO_PARAMS || _contentParameters.size()==0)
        _parameters=_queryParameters;
    else
    {
        _parameters = new MultiMap<>();
        _parameters.addAllValues(_queryParameters);
        _parameters.addAllValues(_contentParameters);
    }
    
    // protect against calls to recycled requests (which is illegal, but
    // this gives better failures 
    MultiMap<String> parameters=_parameters;
    return parameters==null?NO_PARAMS:parameters;
}


private void extractContentParameters()
{
    String contentType = getContentType(); // 得到的ContentType是multipart/formdata
    if (contentType == null || contentType.isEmpty())
        _contentParameters=NO_PARAMS;
    else
    {
        _contentParameters=new MultiMap<>();
        contentType = HttpFields.valueParameters(contentType, null);
        int contentLength = getContentLength();
        if (contentLength != 0)
        {
            if (MimeTypes.Type.FORM_ENCODED.is(contentType) && _inputState == __NONE &&
                _channel.getHttpConfiguration().isFormEncodedMethod(getMethod()))
            {
                extractFormParameters(_contentParameters);
            }
            else if (contentType.startsWith("multipart/form-data") &&
                    getAttribute(__MULTIPART_CONFIG_ELEMENT) != null &&
                    _multiPartInputStream == null)
            {
                extractMultipartParameters(_contentParameters);  // 这里
            }
        }
    }

}

 private void extractMultipartParameters(MultiMap<String> result)
{
    try
    {
        getParts(result);
    }
    catch (IOException | ServletException e)
    {
        LOG.warn(e);
        throw new RuntimeException(e);
    }
}
```

## 总结

* PUT用于Multipart是不规范的
* 用起来简单，但是出问题能不能解决，是否知道原因才是最重要的




