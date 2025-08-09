# Purpose of Experiments

Automate the deployment of a server on digitalocean with nginx enabled and running natively, providing the IP address and port it is available on. No cleanup intended.

## Developer Experience Issues

- The methods on the ``droplets`` attribute of pydo.Client instances do not show up in pycharm.
    - It should not require memorizing and learning what is available explicitly for every operation to be productive.
    - Example of the issue: https://ibb.co/GrSbRqK
- The ``droplets.create`` method takes arguments in the form of a dictionary, obscuring the available options.
  - It's harmful to the developer experience (even to the AI generation experience) to have the usage unnecessarily obscured.
    - It should be explicit with what options are available, like name, size (machine slug), etc. 
    - An example of where AI went wrong 1: It generated the arguments for the create method by passing them as regular arguments by name. (https://ibb.co/3wQvdyJ), (https://ibb.co/spLHK97w)
    - An example of where AI went wrong 2: It tried to pass a dictionary in as **kwargs when told one was required by this api instead. 
- The object representing a droplet as returned by ``droplets.create`` doesn't show up in pycharm, and it is just a dictionary.
  - It is counter-productive to have to be aware of everything needed in a returned dictionary and hampers exploratory testing.
  - It is preferable to have what is available on the returned object explicitly defined and be able to hover for information in an IDE.
  - Example of an issue relating to AI generating code in exploring the problem: https://ibb.co/Kxj82zgf