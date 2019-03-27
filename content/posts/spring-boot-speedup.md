---
title: "如何加快 Spring Boot 项目的启动速度？"
date: 2018-09-04
draft: false
categories: ["SpringBoot"]
tags: ["SpringBoot", "Spring"]
---

可以通过避免包扫描和自动配置来加快Spring Boot项目的启动速度。

## 序

一个agent部署在其他机器上，其能够接收提交的Jar包进行部署，但是我们无法登陆机器也无法更新agent的代码。agent中有个逻辑是部署jar包的时候会等待10s，然后判断是否启动成功，如果没有启动成功，则进行回滚，这样就导致了一个问题：要部署的jar启动时间超过了10s，然后就回滚，无法部署成功。最终的解决方法只能是加快 Spring Boot 的启动速度了，经过调整后，到达了想要的结果。


我们知道在基于 Spring Boot 的项目中，主类一般会加上注解 `@SpringBootApplication`，`@SpringBootApplication` 其实就是开启了包扫描和自动注解特性。

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class))
public @interface SpringBootApplication {
//................
}
```

问题的关键是 `ComponentScan` 和 `EnableAutoConfiguration` 是非常耗时的。`@ComponentScan` 是扫描指定包下面的注解标记，从而生成相应的 Bean，`@EnableAutoConfiguration` 可以根据引入的jar包，自动配置一些 Bean，但是并非都是需要的。

## 避免包扫描（ComponentScan）

不使用 `@SpringBootApplication` 注解引入的 `ComponentScan`，改为自己配置项目中需要的Bean，启动类变为了：

```java
//@SpringBootApplication
@Configuration
@EnableAutoConfiguration
public abstract class AppRunner {
// ......
}
```

Bean 的实例化配置统一放到 BeanConfig.class中：

```java
@Configuration
public class BeanConfig {

    @Autowired
    private SqlSessionFactory sqlSessionFactory;

   //.......

    @Bean
    public FooService fooService() {
        return new FooService();
    }

    @Bean
    public MapperFactoryBean<FooMapper> fooMapper() {
        MapperFactoryBean<FooMapper> mfb = new MapperFactoryBean<FooMapper>();
        mfb.setMapperInterface(FooMapper.class);
        mfb.setSqlSessionFactory(sqlSessionFactory);
        return mfb;
    }

}
```

## 避免自动配置（EnableAutoConfiguration）

可以先在项目中配置输出DEBUG日志，可以看到 Spring Boot 自动配置报告，然后自己引入那些实际需要的配置（报告中的 Positive matches）。

```java
=========================
AUTO-CONFIGURATION REPORT
=========================


Positive matches:
-----------------

   AopAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'org.springframework.context.annotation.EnableAspectJAutoProxy', 'org.aspectj.lang.annotation.Aspect', 'org.aspectj.lang.reflect.Advice' (OnClassCondition)
      - @ConditionalOnProperty (spring.aop.auto=true) matched (OnPropertyCondition)

   AopAutoConfiguration.JdkDynamicAutoProxyConfiguration matched:
      - @ConditionalOnProperty (spring.aop.proxy-target-class=false) matched (OnPropertyCondition)

   DataSourceAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'javax.sql.DataSource', 'org.springframework.jdbc.datasource.embedded.EmbeddedDatabaseType' (OnClassCondition)

   DataSourceAutoConfiguration#dataSourceInitializer matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.autoconfigure.jdbc.DataSourceInitializer; SearchStrategy: all) did not find any beans (OnBeanCondition)

   DataSourceConfiguration.Generic matched:
      - @ConditionalOnProperty (spring.datasource.type) matched (OnPropertyCondition)

   DataSourcePoolMetadataProvidersConfiguration.TomcatDataSourcePoolMetadataProviderConfiguration matched:
      - @ConditionalOnClass found required class 'org.apache.tomcat.jdbc.pool.DataSource' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration matched:
      - @ConditionalOnClass found required classes 'org.springframework.jdbc.core.JdbcTemplate', 'org.springframework.transaction.PlatformTransactionManager' (OnClassCondition)

   DataSourceTransactionManagerAutoConfiguration.DataSourceTransactionManagerConfiguration matched:
      - @ConditionalOnSingleCandidate (types: javax.sql.DataSource; SearchStrategy: all) found a primary bean from beans 'dataSource' (OnBeanCondition)

   DispatcherServletAutoConfiguration matched:
      - @ConditionalOnClass found required class 'org.springframework.web.servlet.DispatcherServlet' (OnClassCondition)
      - @ConditionalOnWebApplication (required) found StandardServletEnvironment (OnWebApplicationCondition)

   DispatcherServletAutoConfiguration.DispatcherServletConfiguration matched:
      - @ConditionalOnClass found required class 'javax.servlet.ServletRegistration' (OnClassCondition)
      - Default DispatcherServlet did not find dispatcher servlet beans (DispatcherServletAutoConfiguration.DefaultDispatcherServletCondition)

   DispatcherServletAutoConfiguration.DispatcherServletRegistrationConfiguration matched:
      - @ConditionalOnClass found required class 'javax.servlet.ServletRegistration' (OnClassCondition)
      - DispatcherServlet Registration did not find servlet registration bean (DispatcherServletAutoConfiguration.DispatcherServletRegistrationCondition)
      - DispatcherServlet Registration found servlet registration beans 'druidServlet' and none is named dispatcherServletRegistration (DispatcherServletAutoConfiguration.DispatcherServletRegistrationCondition)

   DispatcherServletAutoConfiguration.DispatcherServletRegistrationConfiguration#dispatcherServletRegistration matched:
      - @ConditionalOnBean (names: dispatcherServlet; types: org.springframework.web.servlet.DispatcherServlet; SearchStrategy: all) found beans 'dispatcherServlet', 'dispatcherServlet' (OnBeanCondition)

  // ............... 省略


Negative matches:
-----------------

  //...............

```


可以手动引入需要的配置类，启动类变成了下面这样，其中以 `AutoConfiguration` 结尾的配置类来自上述报告中那些匹配上的条目（也就是需要的），后面的如 `MyBatisConfig.class,  BeanConfig.class` 是我们自己定义的配置类。

```java
//@SpringBootApplication
@Configuration
@Import({
    AopAutoConfiguration.class, DataSourceAutoConfiguration.class, DispatcherServletAutoConfiguration.class,
    EmbeddedServletContainerAutoConfiguration.class, ErrorMvcAutoConfiguration.class, HttpEncodingAutoConfiguration.class,
    HttpMessageConvertersAutoConfiguration.class, JacksonAutoConfiguration.class, JdbcTemplateAutoConfiguration.class,
     MybatisAutoConfiguration.class, ServerPropertiesAutoConfiguration.class,
    TransactionAutoConfiguration.class, WebMvcAutoConfiguration.class, 
    MyBatisConfig.class, MyBatisMapperScannerConfig.class,
    MultipartConfig.class, BeanConfig.class})
//@EnableAutoConfiguration
public abstract class AppRunner {
// ......
}
```


## 效果对比

优化前，启动耗时12秒。

```
2018-09-04 10:11:45 [main] INFO com.vonzhou.AppRunner.logStarted 57 - Started AppRunner in 12.608 seconds (JVM running for 13.439)
```

优化后，启动只耗了6秒。

```
2018-09-04 14:47:10 [main] INFO  com.vonzhou.AppRunner.logStarted 57 - Started AppRunner in 5.973 seconds (JVM running for 6.55)
```

