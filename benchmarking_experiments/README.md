# Context of Experiments

We require experimenting with various aspects of load testing/generation so that we can test and stabilize our servers. The existing tooling in the python ecosystem is insufficient for this and tooling elsewhere is not suited as our infrastructure for interacting with the systems under test is in python, and built on top of asyncio, something <redacted> does not support.

# Objectives around this
- Given a coroutine to be awaited, generate an amount of load based on it at a rate per second.
- Given a coroutine to be awaited, adequately measure the latency of the system to do actions.
- Given the ability to generate load, adjust it overtime and record how latency changes.

At this time, **immediately** required is tooling to script up scenarios using asyncio to stress the system, to assure that it will not cease to work under load. The infrastructure developed for our acceptance tests (not shown here) makes it effortless to script stuff up in performance tests, and the only concern and focus is on having more generic load testing tooling.