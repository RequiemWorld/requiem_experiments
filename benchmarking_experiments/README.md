# Context of Experiments

Primarily, and immediately, we require being able to go from coroutine with an end-to-end workflow of a user (similar to our acceptance tests would have) and to perform load testing using it (using the same asyncio based architecture/infrastructure). The goal is to further the understanding on the project of load testing, and provide simple utilities to generate load, and take metrics generically based on coroutine execution time. 

# Objectives around this
- Given a coroutine to be awaited, generate an amount of load based on it at a rate per second.
- Given a coroutine to be awaited, adequately measure the latency of the system to do actions.
- Given the ability to generate load, adjust it overtime and record how latency changes.
    - This will allow us to drive the optimization of the server based on performance tests rather than making guesses. 
    - This will allow us to do different actions with elaborate setup that our internal DSL simplifies, and to see at which point/how many users performance starts to degrade.
- Given the ability to generate load based on a coroutine, hit the server hard and make it crash.
    - I think that we should do this before anything meant to optimize performance (including caching).

# Simplicity/Design

This design should not be complicated at all. We aren't measuring a specific protocol, we're measuring the time for a coroutine to complete, in this case it may be the execution of a method on a driver to register an account or call login with false credentials. Since coroutine execution time is the only thing we measure, sources of time can be mocked during tests, and coroutines as part of test cases can be passed in to track progress/certain conditions. This leaves it as simple as executing coroutines, logging results, and reporting statistics, as well as logic for ramping up the load which I believe within a few hours was figured out. 