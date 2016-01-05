# 初次使用MacDown


**代码高亮：**

```haskell
firstTo :: Int -> Maybe Int
firstTo n = find (\x -> digitSum x == n) [1 ..]

findKey :: (Eq k) => k -> [(k,v)] -> v
findKey key xs = snd . head . filter (\(k,v) -> k == key) $ xs
```

**GFM task list的支持：**

- [x] learn haskell
- [ ] write blog


**Tex数学公式：**(GFM不支持)

$$
\begin{align*}
    \frac{f(x+h)-f(x)}{h} & =  \frac{(x+h)^3-x^3}{h}   \\
                          & =  \frac{x^3+3x^2h+3xh^2+h^3 - x^3}{h}\\
                          & =  \frac{3x^2h+2xh^2+h^3}{h}\\
                          & =  \frac{h(3x^2+2xh+h^2)}{h}\\
                          & =  3x^2+2xh+h^2
\end{align*} 
$$

**可以导出**

* PDF （不错）
* HTML

~~这是删除线~~


你好世界
====
是的
---

**列表**

*   Red
*   Green
*   Blue

+   Red
+   Green
+   Blue

-   Red
-   Green
-   Blue


基本上，这些够用了!

