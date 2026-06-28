# Redis
Redis (Remote Dictionary Server) is an in-memory data structure store.<br>
Traditional database like MySQL or PostgreSQL write data to harddrives whereas `Redis` write it to RAM.<br>
Accessing RAM is much faster compared to harddrive, thus achieving a much faster read speed. Accessing data from Redis by its's key usually takes O(1), responding in sub-milliseconds.<br>
Redis is also a **standalone server**, this means that it can be access by multiple different applications all at once and making it suitable being a bridge between different applications, like a messaging broker or an unified cache.

## When to use Redis
Redis is typically used when speed of accessing data is critical and data retrieval needs to be faster than typically database. <br>
Redis have a lot of built in cachine features like `Time To Live (TTL)` and cache eviction policies.

## Concurrency and Locking
Redis run on a highly optimised single threaded event loop, that is able to handle tens of thosands of concurrent read/write operations per second without having lock conflicts.<br>
This is very useful because of state management and preventing race condition errors.

## Negatives
It is a dictionary store, so if there are complex queries that are needed, having a in memory SQL database might be better than Redis.