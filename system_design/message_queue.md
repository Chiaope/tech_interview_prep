# Message Queue
Message queue is mainly used with the `Producer Consumer` system design.<br>
Message queue is essentially like a broker between the producer and consumer.

The producer will send data and the required processing to be done to the data, as a `message`, to the message queue. The message queue will store these message and wait for consumer to be free to process the data. 

## When to use message queue
There are a few situation where message queue can be beneficial.
- Async work
  - When task does not need to be completed immediately
- Bursty traffice
  - When there are sudden spike in work load and we do not want to drop requests
- Decoupling
  - When we want to scale up or down our resources
- Reliability
  - When we cannot afford to lose our work. Message queue will hold message until we can process them so we dont have to worry about not processing data

## When not to use message queue
When strict latency is needed, when things need to be processed immediately.

## Benefits
Scalability and reliabilty is one of the biggest reason why message queue is used.

Producers and consumers can be scaled horizontally depending on the work load required. 
<br>
When consumers takes in a message to process it and for whatever reason it crashes, the message will be sent back to the message queue to be reprocessed by another consumer, this increase the reliability of the entire system.

## How it works
Typical system that does not use message queue will have a function to take in request and process it at the same time. This is usually not a problem until there are a lot of request and if the processing time takes up quite a bit of time. Assuming the processing time for each request takes up 1 second, and there are 1000 requests, it will take up 1000 seconds. This means that a request could potentially wait up to 1000 seconds and get a time out error.

In order to solve this, message queue system design is used. Message queue can acts as a broker between the producers, who takes in requests, and the consumers, who process these requests. So in the same scenario, we can have either a single or multiple producers taking in all the request and dumping it into the message queue one by one, and this can be done very quickly since there are no processing required. Then the consumers will look into the message queue and find out if there are anything that needs to be processed, if there are messages waiting to be processed, the consumer will take in the message and process them in parallel. This means that essentially every request can be done within 1 second instead of having to wait for 1000 seconds.

When a consumer wants to take a message to process it, it will send the message queue an acquired status and when the consumer have finished processing the message, it will send the message queue an acknowledge status. If for some reason the consumer did not managed to finish the processing, basically never send the acknowledge status, the message queue will reroute the message to another consumer to be processed again. A max number of retries can be set to prevent a bad message to take up the resource and time.



## Delivery guarantees
There might be cases where the consumer processed the message completely **BUT** crashes before being able to send an acknowledge status to the message queue.

There are 3 main ways how different message queue handle deliveries.
- At least once
  - Message may be delivered more than once, meaning, a single message could be processed multiple times.
  - This is important because if the process is not indempotent, there might be issues, <br>eg. Minus $500 from acc_id 123 balance  **vs** Update acc_id 123 balance to $1000
- At most once
  - Message are fired and forget, meaning message could potentially remain unprocessed
- Exactly once
  - Message are processed exactly one time
  - Basically like transactional process,<br>eg. Charge acc_id 123 $500 **AND** send an acknowledge update, if acknowledge update is not sent, revert everything back

Most of the time, using `at least once` approach with `indempotent` message is the best way to do things.
<br>
`at most once` aproach is not ideal unless lossing data is fine, something like data anlysis of 1 million data points, losing a few data wont affect the results much.
<br>
`exactly once` this is the holy grail but to achieve this, it is **basically impossible** or very hard. **So during an interview, do not say you can do this!!**

## Scaling
Message queue can only handle so much throughput and when the throughput is too much, we can scale it in the follow way.

- Partitioning
  - Messages are split into different partition and then consumers are subscribed to their specific partition, enabling the consumer to consume the message in parallel.
  - This allow the message queue to scale horizontally.
  - Partitioning can be done using `partition key` and this is important since all message with a specific partition key will only go to that specifc partition and the order which the message is sent will be kept only in it's own partition.
  - Choosing the proper partition key is very important because a wrong partition key can cause the order to be messed up, eg. account_id instead of time_of_day. We also want to choose a proper parition key so that we can spread the load evenly and prevent hot parition.
- Autoscaling group
  - We can scale the number of consumer available up or down, depending on how fast we want to clear our message backlog and this can be scaled up
  - For **partitioned message queue** we can only scale up the number of consumers to a max number that is the same as the **number of partitions**. This is because this type of message queue accounts for the order when the message is sent in for each partition. <br>**Note:** 1 consumer can process message from many partitions but 1 partition can only have 1 consumer, if there are more consumers than partitions, there will be idle consumers, which will not be doing anything except for being a backup.
  - For **non partitioned message queue** we can scale it up **infinitely** as the order when the message is sent in does not matter. Everything will be processed concurrently.
- Batch processing
  - When we are using paritioned message queue, there might be time where our producers volume are so high that the message queue is being overwhelmed despite paritioning it properly and having 1 consumer for each partition. 
  - We can use batch processing. Basically collect a bunch of message all at once and process it all together, this will reduce the network latency and delay when pulling the message.
  - This can be scaled automatically by scaling the minimum number of message required before pulling the messages for processing.
- Back pressure
  - This does not scale the message queue but it just let the producer know that the message queue is overloaded and reject new requests. Basically telling the producer to try again later.

## Dead letter queue (DLQ)
There will be cases when there are `poison messages` that will always fail to be processed. If this poison message is not processed properly, it will take up a lot of resources and time.

In most message queue, there will be a retry mechanism built in just in case something do go wrong. If a consumer failed to process a message properly, the message will be sent back to the message queue and wait for the next consumer to retry and process it. 

Problem arise when consumers keep failing to process the message, these messages are called `poison message`. In order to prevent poison message to hog the resources, message queue implement a max retries for a given message. If the number of retries exceeded the maximum allowed, it will be sent to the `DLQ` to be stored and debugged.

## What happen if the message queue itself crashes
Modern message queue persist messages to disk and can be replicated to multiple different message brokers, basically like having multiple replicas in database. So when one message queue goes down, the replica will take over its place and the process continues.

Some message queue have retention windows, so if things do goes down and messages are not processed properly, we could do a replay and re-process the messages again.