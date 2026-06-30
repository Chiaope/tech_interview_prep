#  Caching
Cache is a temporary storage that keeps recently used data handy so you can get it faster next time.<br>
Eg. Accessing data from disk takes about 1ms, whereas from RAM, it takes only around 100ns.

## When to cache
Caching should not be a default and should only be used during certain scenarios like
- read heavy workload
- expensive database queries
- high database work load
- latency requirements

## External Caching
This is the most common type of caching, eg. Redis, memcache. This is running separate from the application itself, so this cache can be accessed by multiple different application and it will be shared.

### How it works
Application will try to fetch from the cache server through its own connection package, if it fails, it will reach for the database as a fallback.

## In-process caching
This is the fastest type of cahcing and it reduce the complexity of having a seperated caching server. Cache will be set up on the application itself, thus it is very fast.

The trade off is that the cache is not shared, so when something is processed, it is cached on its own application and not shared, if other application need the same information, it will be a waste of resources.

## Content Delivery Network (CDN)
Content delivery network is mainly used for geological advantage, it will reduce the latency for request from far away. Since the data will be stored in the datacenter nearer to the request.

It is not optimised for processing speed, it is optimised for network latency instead. Commonly used to distribute media.

### How it works
So whenever a new request comes in, the request will be routed to the nearest CDN node and if the cache is updated, cache hit, the request will get the data quickly, if the cache is outdated, cache miss,  the CDN node will request the latest information from the main server and then update itself, this way future request from the locations around it will be able to access the data quickly.

## Client side caching
When data is stored directly on the client's browser itself. This is useful when we want to store client's information. We can save a lot of resources on the server side and the data can be proceed quickly. If there are cases when the server crashes, the cache is still retained. 

The down side of this is that the cahced data might be manipulated and malicious, so the security isnt the best.

## Cachine Methods
- Cache aside
    - application will try to get the data from cahce, if cahce misses, it will get from  the database instead and then it will store it in the cache itself
    - Benefit of this is that data is only cached when needed, reducing potential load if the cahced data is not used often
    - Downside of this is that there will be an additional latency whenever the cache misses
- Write through
    - When data is updated, it will be stored directly into the cache first, then from the cache it will write to the database, write will only be considered complete when both the database and the cache have synced.<br>This is only used when read must always be using the fresh data, if not there isnt really a point.
    - Benefit is that cache will always be updated and database will be the backup
    - Downside is that additional complexity is needed to support synching of the data from cache to database. We will be bloating our cache for no reason if the data is not commonly used.
- Write behind
    - Basically like write through but instead of waiting for database to sync with cahce, the cache can flush data to the database asynchronously.
    - Benefits is that it reduce the latency between the writes, since it is asynchronous now, and it is useful when there are tons of writes happening and missing some data in between is fine.
    - Downside is that there might be missing data and if the cache crashes for some reason, then the database will not be able to get its data also.
- Read through
    - Similar to the cache aside but instead of the application reading from the database directly when there is a cache miss, the cache will be reading from the database instead when there is a cache miss. This is similar to how a CDN works.
    - Benefits will be simplified application where the missing logic is handled by the cache, so if there are tons of applications that are depending on this cache, they dont have to handle complex cahce miss scenarios.
    - Downside is that the cache must be the one handling the cache miss and if the cache goes down, there is no back up.

## Cache eviction policies
RAM is limited and it cant store data forever, it will just continues to grow and it will then become more and more expensive to keep up. So we need a way to clear the memory. Below are some of the policies that are available.

- Least Recently Used (LRU)
    - Most common and balanced default caching method
    - It evicts the item that has not been used recently. So basically there is a order that check when was the item used and it will be sorted, most recently used item will in the front and item used in the past in behind. Then the cache will only allow N number of items to exist, if there are more items, it will evict the item at the back of the order.
    - It is often build on using hash map or doubly linked list so it is easy to add items in front or chop off the back using O(1).
- Least Frequentyly Used (LFU)
    - Evict items that are used least often, even if accessed recently.
    - Basically there is a counter on how frequent an item is used, if the item is used very little, it will get evicted quickly.
- Fist In First Out (FIFO)
    - Evict the oldest item first, simple but not always the best choice
- Time to Live (TTL)
    - Each item expires after a set time. Great for items that goes stale like API token.

## Cache invalidation
When cahce got evicted, if we need to get the data back, we need to know how should we do it.

### Common issue
Cache stampede
<br>
When a popular cache get evicted for some reason, and there are tons of request to rebuild this cache, and these requests will execute cache misses process, potentially hitting our database a lot of times and overwhelming it.
- We can handle it is using coalescing, basically the first request will be allowed through and the rest of the request will be waiting for the cache to be updated and get it from the cache instead.
- We can also do cache warming, basically refreshing the data before the data go outdated, essentially the cached item will never expire

Cache consistency
<br>
When there are new data that is being uploaded to the database, the cache might not be updated, thus when someone make request to the cache, the old data might be returned instead of the new data. The cache will keep returning the old data until it is evicted. There is no real answer to this because it really depends on how often we want to update our cache and how much resource we want to spend on updating our cache. Whether eventual consistency is enough or not.
- Invalidate on write, basically when the item get updated in the database, it will tell the cache that the old item is no longer valid and the cache should pull the latest data
- We can also have a short TTL instead so when the data get old, it will get the latest data

Hot keys
<br>
When there are some cache items that is very popular and it keeps getting requested, this might cause a bottle neck for the cahce system.
- We can basically just replicate the hot key into each of the different cache instance that we have scaled. We can have a load balancer to spread the load to each cache instance.
- We can also have a fall back cache, which is the in-process cache in additional to the external cache. So the application can store hot keys in the in process cache instead of fetching from the external cache. This will reduce the load on the external cache and also make the request faster.
