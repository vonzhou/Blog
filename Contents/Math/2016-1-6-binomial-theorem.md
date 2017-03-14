# 二项式定理

**为何学？**

在进行分布式Bloom filter误判率分析的时候，用到了二项式定理，一时未查明，所以浪费了不少时间。

二项式（Binomial）是俩单项式（[monomials](https://en.wikipedia.org/wiki/Monomial)）之和，是一种比较简单的多项式（polynomial），只有一个变量的二项式可以表示为下面形式：

$$
ax^n-bx^m
$$

二项式定理描述的就是把二项式的n次方展开为多个项目的和，具体的为：

$$
(x+y)^n = \lgroup_{0}^{n}\rgroup x^ny^0 + \lgroup_{1}^{n}\rgroup x^{n-1}y^1 + \lgroup_{2}^{n}\rgroup x^{n-2}y^2 + ... + \lgroup_{n-1}^{n}\rgroup x^1y^{n-1} + \lgroup_{n}^{n}\rgroup x^0y^n
$$

前面的称为二项式系数（ [binomial coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient)）：

$$
\lgroup_{k}^{n}\rgroup
$$

用求和表达式写作：

$$
(x+y)^n =\sum_{k=0}^{n}\lgroup_{k}^{n}\rgroup x^{n-k}y^{k}
$$

相关：

* 帕斯卡三角形
* ​[Binomial theorem](https://en.wikipedia.org/wiki/Binomial_theorem)

