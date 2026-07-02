# High Frequency Trading System Design
Most high frequency trading are used by market making company, because to them speed is everything, earning that 2 cent spread every seconds vs microsecond, vs nano seconds matters.

## Steps
1. Market data consumption
2. Update order book
3. Event queue
4. Downstream applications
5. FPGA acceleration
6. Smart order router
7. Audit and Analytics
8. Order Management System (OMS)
9. Metrics monitoring

### Market data consumption
Data from stock exchangs comes in through a network delivery system which is most likely in the co location facility, physically near the exchange server to reduce travel time, and then `multicast feeds` are used to stream data to the `ultra-low-latency network interface card`, this allow the system to handle market update in microseconds. It is then passed to the `market data feed handler` to be streamed to downstream application.

### Update order book
There are order book replica available that are synced via in-memory replication, making sure replication is quite and fault tolerant, if one crashes. Updated order book is then streamed into event queue for the trading system to process and execute.

### Event queue
There is a `lock-free` queue that is optimised for throughput and low contention, preventing jitters when application is grabbing the same data together. These data also have nanosecond timestamp to ensure accuracy and exact sequence of market data update, benchmarket internal latencies and sync with external systems.

### Downstream applications
Downstream applications will consume these events and then process them, whether to execute smart order routing, for risk management, for trading, for monitoring or for external systems. 


### FPGA acceleration
This is where the hardware is heavily optimised. This is the core of the execution engine.

Strategy is processed in the FPGA and the logic is placed in the FPGA to execute at the best possible price.

### Smart order router
The smart order router decides where should the order be placed, whether on NASDAQ, NYSE, whether it should be market order, stop order, limit order, etc. It take into consideration of liquidity, latency, fill probabilty, rebate structures, etc before sending the order.

There are also pre trade risk checks that ensure that all of the exposure, capita, sizing, or strategy is aligned before allowing the order to go through.

### Audit and Analytics
Once the order has been executed, the logs are stored and it will be used for auditing and analysis. This is meant to ensure everything that happened are in place and then strategies can be validated and also improved based on the actual executions.

### Order Management System (OMS)
It tracks the routes take, the execution timestamp, status updates, etc. It coordinates the between exchanges, strategy engines and reportion systems.

### Metrics monitoring
Trade metrics are collected and monitored to understand throughput, latency, error rates, etc. It will trigger an alert when anomaly happens.