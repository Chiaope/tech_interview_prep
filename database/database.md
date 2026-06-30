# Database
There are many different database that functions differently.<br>
Mainly there are 2 types, `OLAP` and `OLTP` but there is also a hybrid which is `HTAP`.

The main difference between OLAP and OLTP are how they are stored and what are their purpuse. OLAP is a **column** based database and OLTP is a **row** based database. OLAP is more for analytics where as OLTP are more for transactions.

Data storage differ from column based and row based database. Column based database typically group the values in the column together and store them while row based database typically group the values in the row together and store them. This means that it is easier for column based database to retrieve column data and row based database to retrieve row data.

## Online Analytical Processing (OLAP)
Main benefit for OLAP is analysing data. Because analytics normally just look at a few set of columns, eg. we need "Gender" column to find out how many males vs females, they dont care about other columns, thus having a column based database will be more efficient in terms of fetching the data.

OLAP is generally more effient as repeated values are easily stored as counts and indexes so it is much faster and efficient to process.

## Online Transactional Processing (OLTP)
Main benfit for OLTP is to store and understand transactions. Every transaction that take places can have a lot of different data, eg. timestamp, user_id, amount, price, so for transactional data, it makes more sense to store data using row based database so we can see which event happened before another event and what is the next event that happen, etc.

## Sharding vs Partition
Sharding is the distributing data across multiple machines.<br>
Partitioning is splitting data into subset within the same instance.

## Sharding
Sharding is the splitting of the database data into different portions. Sharding is mostly used when the data rows are not related to each other, so they can be split without any operation issues.

Most common sharding is by geo based sharding. It basically split the database based on geological location so latency will be lesser.

### Benfits of sharding
Sharding provides scalability, better performance, higher reliability and accessibility and also sometimes it will be cheaper to run. <br>
Because sharding split the database into different portion, the querying data will be much faster because we already know where to look for the data, it also provide better scalability because we can always split it down even more when data become larger.<br>
Reliability is also improved as one shard goes down does not affect another shard.<br>
It can potentially be cheaper because expensive hardware is not required and they can run on cheaper commodity storage solutions.

### Disadvantage of sharding
When there is tight relationship between rows and tables, sharding might cause some isses as it will be harder to do complex joins and fetch.<br>
Hotspot could appear if there are many queries to a particular shard, and if the storage solution used is not good enough, there could be increased latency or even potential crashes.<br>
When sharding has been set up, it is hard to undo it or make changes to it because in a live environment where everything is routed properly already, if the database schema changes, a whole new shard key is needed and the set up might cause a lot of issues if we want to ensure high availability.