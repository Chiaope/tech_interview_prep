# Websockets
When dealing with real time data stream, we have to use websockets. Websocket only allow strings not JSON not dictionary not array.

## Architecture
- There should be a backoff in place, most of the time it should be an exponential backoff to retry connection
- there should be ping and pong to maintain the connection
- Open and close timeout should be inplace in case we are not getting response
- Most websocket connections require an initial message, eg. subscribe to something. So we need to take note of it
