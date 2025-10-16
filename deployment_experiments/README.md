# Deployment Experiments

The goal of this section is deployment/configuration automation. We're using the cloud so that we can provision instances of servers and have them available in minutes rather than hours. There are multiple ideals and principles that are at least kept in mind (even if not adhered to) such as immutable infrastructure. I'm extremely proficient in python and various architecture and design around it at this point and various concepts related to devops/continuous delivery. If this project is going to work with the resources available, then simplifying the process of going from working software to deployed software is a must.


## Retracted Information

We need to find a way to go from no servers deployed to operational servers through the same approach to coding anything else on the project. Nothing can be said here on this concisely. See experiments that work us towards are goals for this as they're added/documented. Keeping this repository minimal, like with the previous experiments, is how we're going to tackle this problem quickly.

## Abstract Objectives

- At the press of a button, take a piece of software, which has passed through the acceptance tests in a production like environment, release it into production.
  - This should be able to be done for exploratory testing or done to different environments manually (I think Dave Farley mentioned this somewhere).
- Deploy a piece of software, or a script to production, have it produce a result, get the result off of the machine, and have it auto destruct after some time.
  - Rest easy knowing that if our scripts create a bunch of server instances by mistake, that they get deleted after some time.
  - Deploy servers, make them do something, and get a result, even if the process is error-prone to start with.
  - Deploy the software to a test server and deploy our load tests to another and get a report off of the load testing one.
