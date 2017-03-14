# 使用 redis pipeline优化查询

## 前言

最近在项目中遇到了一个问题：当[条件A]很大的时候数据查询特别慢，A>1000的时候就需要3秒左右，这是不能忍受的。经过排查发现代码中有一个根据A串行查询redis的操作，如下：

```java

if (CollectionUtils.isNotEmpty(list)) {
    for (String key : list) {
        data = redisService.getDataToday(key)
    }
}
```

对这种情况的测试效果：

A   时间
100  249.78ms
500   1.17s
1000  2.4s

其实可以看到时间消耗在了每次查询的网络开销上。接下来进行了2中不同方式的优化。

## 优化1 - 牺牲精确性

上面的场景其实就是把今天的数据放在redis中，如果只是查询历史数据，就可以避免查询redis的开销，如果对精确性没有那么高。

优化后（A=1000）的时间262.93ms。

## 优化2 - 批量操作

既然知道性能的瓶颈在网络开销上，就可以采用批量操作的方式来改进，pipeline，但是要在这里可以使用mget或者pipeline的方式，注意考虑失败的情况。

```
public List<Object> getValueByKeys(final List<String> keys) {
    if (CollectionUtils.isEmpty(keys))
        return null;
    return redisTemplate.executePipelined(new RedisCallback<Object>() {
        public Object doInRedis(RedisConnection connection) throws DataAccessException {
            StringRedisConnection stringRedisConn = (StringRedisConnection) connection;
            for (String key : keys) {
                stringRedisConn.get(key);
            }
            return null;
        }
    });
}
```

优化后（A=1000）的时间304.76ms，的确有所改善。

## 总结

* 在代码中如果有根据变量循环的情况，一定要注意存在的问题

## 参考

[redis pipeline](https://redis.io/topics/pipelining)

[Spring Redis support](http://docs.spring.io/spring-data/data-redis/docs/1.1.0.RELEASE/reference/html/redis.html)