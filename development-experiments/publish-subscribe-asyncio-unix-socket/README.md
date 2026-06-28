# Purpose of Experiment

The purpose of this experiment was to familiarize with using unix sockets, specifically in a publish/subscribe capacity. It doesn't get easier for listening for information updates than reading from a socket file on the system. To work through this, the script design is to host a notification server over a unix socket which will publish the date to every client every second. The client script just has to connect and read it continuously.

- The provided code should be self-explanatory. You pick a socket file location to publish dates to, and you pick that same location to read them from.
- This exercise should showcase that when there is no meaningful complexity from application layer protocols then unix sockets are extremely easy to use.
- This was meant to figure it out for something else. This is roughly the code I think I would write if I was doing this for actual software rather than experiment scripts.
- This can be referred to when there is interest in working with unix sockets in python, as well as needing elegant designs for other languages such as javascript.

## Areas not verified

- I did not look into how the unix sockets are setup internally by asyncio. The main thing is that they should be streaming like TCP or based on chunks of data like udp.
- It shouldn't matter if it is streaming or datagram based because of the light abstraction layer provided on top with the stream reader/writer. But I could be wrong and this needs verification in the future when it becomes relevant.
