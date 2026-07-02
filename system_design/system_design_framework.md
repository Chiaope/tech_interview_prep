# System Design Framework
1. Requirements
   - Outline the functional requirements, which are the features of the systems like being able to book a ticket, and non functional requirements, which are the quality of the system, like low latency.
   - This will be something that the interviewer and you agree on at the start, so everyone know what is going on.
2. Core entities (what objects are needed)
   - What class is needed, like users, tickets, cinema, event. These are normally relational stuff that will be used for mapping in the database.
3. API interface
   - Basic API interface, like whether to use REST endpoints or websocket, etc.
4. Data flow
   - How the data flow from one application to another.
5. High level design (functional requirements)
   - Draw out how does the components are linked together and how it can meet the functional requirements
6. Deep dives (non functional requirements)
   - Dive into specific components and then find out how to satisfy non functional requirements

## How system design interviews evaluated
- Problem solving
  - Identify and prioritise the core challenges
- Solution design
  - Did we weight and balance trade offs
- Technical excellence
  - Show off deep knowledge and expertise, how something work, how something can break, how to prevent fault, how to improve scale and resisliency etc
- Communication
  - Whether you can clearly explain complex concepts to stakeholders

## Fundamentals
- Storage
  - Atomicity, Consistency, Isolation, Durability (ACID) [OLTP] vs Basically Available, Soft state, Eventually consistent (BASE) [Distributed Systems]
- Scalability
  - Veritcal (Increase computer) vs Horizontal (Increase number of compute)
  - Storage: sharding, partitioning, consistent hashing
- Networking
  - Application layers
    - HTTP/HTTPS protocols (Hypertext Transfer Protocol Secure)
      - Underlying protocol used by the World Wide Web to define how messages are formatted and transmitted. 
      - There is a cryptographic layer usually TLS (Transport Layer Security) or SSL (Secure Sockets Layer)
      - HTTP send data in plain text whereas HTTPS encrypts data in transit
    - REST vs GraphQL vs gRPC
      - REST is the traditional web standard, where data are treated as resources. The response will contain a fixed JSON payload.
        - Pros: Ubiquitous, highly cacheable and simple to build and test. 
        - Cons: Over fetching and under fetching, response contain too many data or need multiple API call to fetch all data
      - GraphQL solves REST fetching issues. Client send a query specifying exactly the shape and fields of the data it needs and the server returns exactly that, nothing more nothing less
        - Pros: Prevent over/under fetching, strongly typed schema
        - Cons: Harder to cache at network level since everything is a POST request to a single endpoint, additional complexity to query, poorly optimised queries can be heavy on the database
      - gPRC uses HTTP/2 instead of a typical endpoint. The client calls a function that is executed on the server as if it were a local function
        - Pros: Extremely fast and payload size are tiny compared to JSON, supports bidirectional streaming and strictly typed contracts enforce consistency between microservices
        - Cons: Data is binary (harder to debug), browsers cant use HTTP/2 gRPC natively, require a proxy layer like gRPC-Web
    - Websockets vs SSE (Server-Sent Events)
      - Websockets is a full duplex (two-way) connection over a single TCP socket. After initial HTTP handshale, both client and server can send message to each other independently.
      - SSE is a half duplex (one-way) connection over HTTP. Client can only listen and cannot send data back over the same channel. mimetype="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
  - Transport layers
    - TCP, UDP
  - Network layers
    - Load balancing, firewall
- Latency, throughput and performance
  - RAM (100ns) vs SSD (0.1-0.2ms) vs HDD (1-2ms)
- Fault tolerance
  - Replication strategy
    - Leader-Follower (Primary-Secondary)
      - All writes goes to a single Leader node and the leader records the changes and send it to all of it's followers, which updates their local copies.
      - High read scalability but leader is the single point of failure for writes
    - Leaderless (Decentralised)
      - Client send writes and read to multiple nodes simultaneously, relies on Quorum system (minimum amount of nodes confirmation to be considered successful) to ensure consistency
      - High consistency but high latency
    - Synchronous
      - Leader waits for followers to confirm write before responding with success, guaranteed data consistency but high latency
    - Asynchrounous
      - Leader logs the write and immediately response to client, updates followers in the backgroud. Low latency but risk data loss if leader crashes before updating followers
  - Failure detection mechanism
    - Heartbeats, ping-ack
    - Gossip protocols
      - Nodes randomly share cluster state information with few neighbours and if a node goes down, the knowledge is spread exponentially across cluster, eliminating a single monitoring bottleneck
  - Redundancy
    - Active-Active redundancy: all redundant components process traffic simultaneously, if one fails, the load balancer simply stops routing request to the failed node, providing seamless failover and ultilise all available hardware resources
    - Active-Passive (Failover): backup components sit idle or in standby mode and only take over if active component goes offline.
      - Hot Standby: Real time sync, instant failover
      - Warm Standby: Running but not receiving traffic, need awhile to sync and scale up
      - Cold Standby: Powered off and required spin up
  - Recovery Mechanism
    - Failover Leader Election: When leader dies, followers pick a new one and agrees on exactly one new leader
    - Write ahead logging: Write incoming transactions to an append only log on disk before updating in memory data structure, if node crashes, replay can be done and rebuld the state
      - Similar to using a state file
    - Read repair: nodes that have latest state will notice other node that have older state, will automatically push the newest data to stale node
- CAP (Consistency, Availablity, Partition Tolerance) Theorem
  - There can only be 2 out of the 3 and partition tolerance is definitely needed, so need to choose either consistency or availablity.

## Storage
SQL vs NoSQL doesnt really matter, it really depends on how the application read and write data.

Caching is system short term memory, need to know how to invalidate them how to keep cache fresh, etc.

## Message queue
This is how components can talk to each other without blocking the entire application. This is useful if there are a lot of different components that depends on each other and it can do things asynchronously without waiting for each other.

This is useful to control traffic spikes, because task will be send to the message queue instead of blocking the entire request and keep things running. 

We need to know what is the delivery mechanism needed and how can we make sure it doesnt go down or after it goes down how to bring it back up.

## Load balancer
This is used to determine how the load is being spread to multiple different replicas or how to deploy new updates.

## Blob storage
This is where image and non structured data lives.