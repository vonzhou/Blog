---
title: "Spring 中如何控制2个bean中的初始化顺序？"
date: 2017-10-17
draft: false
categories: ["Spring"]
tags: [ "Spring"]
---

开发过程中有这样一个场景，2个 bean 初始化逻辑中有依赖关系，需要控制二者的初始化顺序。实现方式可以有多种，本文结合目前对 Spring 的理解，尝试列出几种思路。

## 场景

假设A，B两个 bean 都需要在初始化的时候从本地磁盘读取文件，其中B加载的文件，依赖A中加载的全局配置文件中配置的路径，所以需要A先于B初始化，此外A中的配置改变后也需要触发B的重新加载逻辑，所以A，B需要注入彼此。

对于下面的模型，问题简化为：我们需要initA()先于initB()得到执行。

```java
@Service
public class A {
    @Autowired
    private B b;

    public A() {
        System.out.println("A construct");
    }

    @PostConstruct
    public void init() {
        initA();
    }

    private void initA() {
        System.out.println("A init");
    }
}

@Service
public class B  {
    @Autowired
    private A a;

    public B() {
        System.out.println("B construct");
    }

    @PostConstruct
    public void init() {
        initB();
    }

    private void initB(){
        System.out.println("B init");
    }
}
```



## 方案一：立Flag

我们可以在业务层自己控制A，B的初始化顺序，在A中设置一个“是否初始化的”标记，B初始化前检测A是否得以初始化，如果没有则调用A的初始化方法，所谓的check-and-act。对于上述模型，实现如下：

```java
@Service
public class A {

    private static volatile boolean initialized;

    @Autowired
    private B b;

    public A() {
        System.out.println("A construct");
    }

    @PostConstruct
    public void init() {
        initA();
    }

    public boolean isInitialized() {
        return initialized;
    }

    public void initA() {
        if (!isInitialized()) {
            System.out.println("A init");
        }
        initialized = true;
    }
}

@Service
public class B {

    @Autowired
    private A a;


    public B() {
        System.out.println("B construct");
    }

    @PostConstruct
    public void init() {
        initB();
    }


    private void initB() {
        if (!a.isInitialized()) {
            a.initA();
        }
        System.out.println("B init");
    }
```

执行效果：
```bash
A construct
B construct
A init
B init
```

这种立flag的方法好处是可以做到lazy initialization，但是如果类似逻辑很多的话代码中到处充斥着类似代码，不优雅，所以考虑是否框架本身就可以满足我们的需要。


## 方案二：使用DependsOn

Spring 中的 `DependsOn` 注解可以保证被依赖的bean先于当前bean被容器创建，但是如果不理解Spring中bean加载过程会对 DependsOn 有误解，自己也确实踩过坑。对于上述模型，如果在B上加上注解 `@DependsOn({"a"})`，得到的执行结果是：

```bash
A construct
B construct
B init
A init
```

在这里**问题的关键**是：bean属性的注入是在初始化方法调用之前。

```java
// 代码位置：AbstractAutowireCapableBeanFactory.doCreateBean
// 填充 bean 的各个属性，包括依赖注入
populateBean(beanName, mbd, instanceWrapper);
if (exposedObject != null) {
    // 调用初始化方法，如果是 InitializingBean 则先调用 afterPropertiesSet 然后调用自定义的init-method 方法
    exposedObject = initializeBean(beanName, exposedObject, mbd);
}
```

结合本例，发生的实际情况是，因为出现了循环依赖，A依赖B，加载B，B依赖A，所以得到了一个提前暴露的A，然后调用B的初始化方法，接着回到A的初始化方法。具体源码分析过程如下：

ApplicationContext 在 refresh 过程中的最后会加载所有的 no-lazy 单例。

![Spring上下文初始化过程](/images/spring-two-bean-init-order-control-1.jpg)

本例中，先加载的bean A，最终通过无参构造器构造，然后，继续属性填充（populateBean），发现需要注入 bean B。所以转而加载 bean B（递归调用 getBean()）。此时发现 bean B 需要 DependsOn("a")，在保存依赖关系（为了防止循环 depends）后，调用 getBean("a")，此时会得到提前暴露的 bean A ，所以继续 B 的加载，流程为： 初始化策略构造实例  -> 属性填充（同样会注入提前暴露的 bean A ） -> 调用初始化方法。

```java
// 代码位置：AbstractBeanFactory.doGetBean
// Guarantee initialization of beans that the current bean depends on. 实例化依赖的 bean
String[] dependsOn = mbd.getDependsOn();
if (dependsOn != null) {
    for (String dep : dependsOn) {
        if (isDependent(beanName, dep)) {
            throw new BeanCreationException(mbd.getResourceDescription(),
                    beanName, "Circular depends-on relationship between '"
                    + beanName + "' and '" + dep + "'");
        }
        registerDependentBean(dep, beanName); // 缓存 bean 依赖的关系
        getBean(dep);
    }
}
```

得到提前暴露的 bean A的过程为：

![提前暴露bean](/images/spring-two-bean-init-order-control-1.jpg)

此时此刻，bean A 的属性注入完成了， 返回到调用初始化方法，所以表现的行为是：构造A -> 构造B -> B初始化 -> A初始化。

DependsOn只是保证的被依赖的bean先于当前bean被实例化，被创建，所以如果要采用这种方式实现bean初始化顺序的控制，那么可以把初始化逻辑放在构造函数中，但是复杂耗时的逻辑仿造构造器中是不合适的，会影响系统启动速度。


## 方案三：容器加载bean之前

Spring 框架中很多地方都为我们提供了扩展点，很好的体现了开闭原则（OCP）。其中 `BeanFactoryPostProcessor` 可以允许我们在容器加载任何bean之前修改应用上下文中的`BeanDefinition`（从XML配置文件或者配置类中解析得到的bean信息，用于后续实例化bean）。

在本例中，就可以把A的初始化逻辑放在一个 `BeanFactoryPostProcessor` 中。

```java
@Component
public class ABeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory configurableListableBeanFactory) throws BeansException {
        A.initA();
    }
}
```

执行效果：

```bash
A init
A construct
B construct
B init
```

这种方式把A中的初始化逻辑放到了加载bean之前，很适合加载系统全局配置，但是这种方式中初始化逻辑不能依赖bean的状态。

## 方案四：事件监听器的有序性

Spring 中的 `Ordered` 也是一个很重要的组件，很多逻辑中都会判断对象是否实现了 `Ordered` 接口，如果实现了就会先进行排序操作。比如在事件发布的时候，对获取到的 `ApplicationListener` 会先进行排序。

```java
// 代码位置：AbstractApplicationEventMulticaster.ListenerRetriever.getApplicationListeners()
public Collection<ApplicationListener<?>> getApplicationListeners() {
        LinkedList<ApplicationListener<?>> allListeners = new LinkedList<ApplicationListener<?>>();
        for (ApplicationListener<?> listener : this.applicationListeners) {
            allListeners.add(listener);
        }
        if (!this.applicationListenerBeans.isEmpty()) {
            BeanFactory beanFactory = getBeanFactory();
            for (String listenerBeanName : this.applicationListenerBeans) {
                try {
                    ApplicationListener<?> listener = beanFactory.getBean(listenerBeanName, ApplicationListener.class);
                    if (this.preFiltered || !allListeners.contains(listener)) {
                        allListeners.add(listener);
                    }
                } catch (NoSuchBeanDefinitionException ex) {
                    // Singleton listener instance (without backing bean definition) disappeared -
                    // probably in the middle of the destruction phase
                }
            }
        }
        AnnotationAwareOrderComparator.sort(allListeners); // 排序
        return allListeners;
    }
```

所以可以利用事件监听器在处理事件时的有序性，在应用上下文 refresh 完成后，分别实现A，B中对应的初始化逻辑。

```java
@Component
public class ApplicationListenerA implements ApplicationListener<ApplicationContextEvent>, Ordered {
    @Override
    public void onApplicationEvent(ApplicationContextEvent event) {
        initA();
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE; // 比 ApplicationListenerB 优先级高
    }

    public static void initA() {
        System.out.println("A init");
    }
}

@Component
public class ApplicationListenerB implements ApplicationListener<ApplicationContextEvent>, Ordered{
    @Override
    public void onApplicationEvent(ApplicationContextEvent event) {
        initB();
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE -1;
    }

    private void initB() {
        System.out.println("B init");
    }
}
```

执行效果：

```bash
A construct
B construct
A init
B init
```

这种方式就是站在事件响应的角度，上下文加载完成后，先实现A逻辑，然后实现B逻辑。

## 总结

在平时的开发中使用的可能都是一个语言，一个框架的冰山一角，随着对语言，对框架的不断深入，你会发现更多的可能。本文只是基于目前对于 Spring 框架的理解做出的尝试，解决一个问题可能有多种方式，其中必然存在权衡选择，取决于对业务对技术的理解。

