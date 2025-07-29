# Research & Development for generic asyncio based performance testing tools on the project

There is plenty of tooling for testing HTTP but limited tooling for testing custom protocols, even less so when reusing asyncio-based test infrastructure is desired. The objective of this experimental code is to provide the simple tools and algorithms necessary for generating load against an application (such as a stateful game server) and monitoring the load of an application.

## Utilities Added
- SlidingWindowActionsPerSecondMonitor
  - A utility for tracking (globally) how many of something happened in the past second, when 900ms goes by and another action happens, and another 100ms goes by, the number of actions per second won't reset to zero, it will be based on the actual rate they're happening (up to the tracking capacity limit).
  - The idea behind this was to put it onto a server for manual testing of load generation scripts and see if what the server is seeing matches the rate we are supposed to be sending.
