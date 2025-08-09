# Purpose of Experiments

Automate the deployment of a server on digitalocean with nginx enabled and running natively, providing the IP address and port it is available on. No cleanup intended.

## Developer Experience Issues

- The methods on the ``droplets`` attribute of pydo.Client instances do not show up in pycharm.
    - It should not require memorizing and learning what is available explicitly for every operation to be productive.
    - Example of the issue: https://ibb.co/GrSbRqK
