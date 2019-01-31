[主页](http://vonzhou.com)  | [读书](https://github.com/vonzhou/readings)  | [知乎](https://www.zhihu.com/people/vonzhou) | [GitHub](https://github.com/vonzhou)
---
# 何为整洁架构？
---

写整洁代码，搞整洁架构。关于《Clean Architecture》的读书笔记。

整本书读下来，总的来说，除了老生常谈的几大经典设计模式外，重点就是划分好系统的边界，组织好依赖关系，区分哪些属于高层的业务层，哪些是外层的细节层。


![](/images/clean-arch-mind.jpg)


## II 编程范式

结构式编程，面向对象编程，函数式编程。


## III 设计模式

### 7.单一职责原则 SRP:Single Responsibility Principle

一个模块应该有且只有一个原因来改变 A module should have one, and only one, reason to change。体现的是内聚性（Cohesion）。SRP是方法和类级别的，上升到组件级别就是通用闭包原则（Common Closure Principle），上升到架构级别就是架构边界（Boundary）。 


### 8.开闭原则 OCP:Open-Closed Principle

对扩展开放，对修改关闭。通过组织好系统中组件的依赖关系来实现，高层的业务逻辑不会轻易改变，让底层的策略可配置，可扩展，可替换。

### 9.里氏替换原则 LSP: Liskov Substitution Principle

### 10.接口隔离原则 ISP：Interface Segregation Principle



### 11.依赖倒置 DIP：Dependency Inversion Principle



## IV 组件模式

### 12.组件

### 13.组件内聚 Component Cohesion

### 14.组件耦合 Component Coupling


## V 架构

### 15.何为架构？


### 16.独立性 Independence

用例，开发，部署，运维都应保持独立性，做好解耦。

好的架构可以从单体架构开始（源码级的独立），然后慢慢改造成可独立部署的单元（部署级的独立），最终向独立服务或微服务靠。

系统的解耦模式会随时间而改变，好的架构师预见，并且助力这种改变。

### 17.划分边界 Boundaries:Draw lines

划分边界其实就是单一指责原则（SRP，Single Responsibility Principle）的运用，SRP指导我们如何画界，界线明晰可以让我延迟决策，比如业务核心和数据库的选择无关，和IO无关，和GUI无关。

### 18.边界剖析 Boundary anatomy

也没有剖析个啥。边界的形式有单体里面的方法调用，可部署的组件，线程，进程，服务。一般的系统都会既有服务级别的边界，也有本地这些。终归到底仍然是源码级别要考虑好。

### 19.策略和层次  Policy and Level

处于同一层次，因为相同原因改变的策略应该组织为同一个组件，SRP。核心的业务层次越高，高层变化不频繁，底层变化更频繁。这里涉及很多涉及原则：Single Responsibility Principle, Open-Closed Principle, Common Closure Principle, Dependency Inversion Principle, Stable Dependencies Principle, Stable Abstractions Principle。

### 20.业务逻辑 Business Rules

如果想把应用组织成业务核心和插件的形式，就要找到系统的核心业务是什么？Business Rules是系统的核心功能，是挣钱/省钱的地方，其应该是系统中最独立，复用性最好的代码。关键业务+关键业务数据组成了实例模型Entity。用例Use Case比Entity层次低，Use case依赖于Entity。

### 21.尖叫的架构 Screaming Architecture

令人尖叫的架构，应该是看到代码组织后，就一目了然的知道这个系统的确是这样的。架构要基于用例而非框架，框架是工具而已，应该放到最后考虑，并且是能够替换的。好的架构要易于测试，而不受制于使用的框架，数据库。

### 22.整洁架构 Clean Architecture

划分边界，并且遵循依赖原则，就会得到一个整洁架构。说易行难。

![](/images/clean-arch.jpg)


### 23.展示器和谦卑对象  Presenters and Humble Objects

在架构的边界处采用谦卑对象模式（Humble Object Principle）可增加整个系统的可测试性。什么是谦卑对象模式？就是把易于测试的行为和难以测试的行为分别对待。比如GUI很难测试，但是采用HOP后，可将其分为Presenter和View两类，View就是这里的谦卑对象很难测试，这样Presenter的行为可以充分测试，然后把简单的数据传递给View进行展示，没有复杂逻辑。

### 24.不完全边界 Partial Boundaries

架构边界是完全严格实现，还是部分实现，是架构师需要考虑的问题。这里提出了实现部分边界的3中方法：单一组件部署；一维边界；Facade模式。

### 25.分层和边界 Layers and Boundaries

通过一个游戏的例子说明了如何设计分层和架构。架构师的职责就是要在系统的进化过程中，提前发现系统的边界，并且权衡哪些要完全实现，哪些部分实现，哪些可以忽略。


### 26.The Main Component

应用系统的Main可以视为插件组件（plugin component）：加载配置，设置初始条件，收集外部资源，然后将控制逻辑交给上层的策略层。


### 27.服务可大可小 Services:Great and Small

（没咋看懂！@#）虽然，系统的服务和其可扩展性，可开发性一样有用，但是服务不是重要的架构元素。系统架构是由边界，及跨边界的依赖组成的。一个服务可能是一个单独的组件，也可能是由边界分隔的多个组件组成。


### 28.测试边界 Test Boundary

可测试性也应作为系统设计的一方面，要重视。

### 29.Clean Embedded Architecture

嵌入式系统开发者也应该学习软件架构的思想，分层，增加抽象层。

## VI 细节

### 30.数据库是细节

数据模型和架构相关，但是数据库是一个工具，是细节。

### 31.Web是细节

The Web is an IO Device.

### 32.框架是细节

Donot marry the framework. 划好边界。



> 2019.1.8 22:32 杭州


