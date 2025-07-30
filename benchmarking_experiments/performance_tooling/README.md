# Research/Design

The research for the development of this is nothing special, however, for clarity/documentation sake since it is new to me I'm placing some of it here. **NOTICE**: Some of this information may be wrong but it is meant to reflect my current understanding, when it improves it will likely be updated.

## Concepts - Virtual Users

A virtual user is something that will loop repeatedly and execute a task over and over again. A virtual user when added to the system will execute a task a given number of times, when they've finished executing it the given amount they are done. When no amount of iterations is specified for a user, they will execute the task infinitely.

- A virtual user can have a delay between iterations which can be randomized.

### Intelligence (hypothetical examples to demonstrate points)

- **Testing 500 requests per second**: A given number of requests per second cannot be tested directly, as there is an abstraction in place, and it is the Virtual User... To get 500 requests per second, the VirtualUser must do nothing but make a request, and it must have a delay between iterations of one second.
- **When you go from one virtual user, to 500 over a period of time, they're gone**: When you setup a load test to ramp up the amount of users from 1 user to 500 over the span of 10 minutes, should any of them hit their final iteration before then, they won't be added and there won't be 500 at a time by the end.
  - In order to ramp up from 1 user, to 500 over a period of time and ensure that by the end, the server is being hit with 500 still, each user must have an unlimited number of iterations, and an appropriate delay between them.