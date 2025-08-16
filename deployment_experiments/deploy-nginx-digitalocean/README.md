# Purpose of Experiments

Automate the deployment of a server on digitalocean with nginx enabled and running natively, providing the IP address and port it is available on. No cleanup intended.

## Discovery - 1 (service starting in cloud-init config may hang forever)
- When using cloud-init to install a package containing a systemd service (nginx), starting it as part of the ``runcmd`` section presumably hangs forever. This article was followed and attempting the solution, ``daemon-reload``, and ``start --no-block nginx`` ~~resulted in nginx being started after some time~~. [\[1\]](https://ibb.co/XrszWggx) [\[2\]](https://ibb.co/WvskSDPp) 
  - NGINX wasn't just started after some time, it was started fairly quickly, loading before it was up, and then reloading just wasn't working at the time of writing due to an issue with firefox mentioned in discovery 2.

## Discovery - 2 (firefox silently switching to https:// after http connection fails and still doing so on reload)
- Problem: Pasting the server IP Address into firefox resulted in it seemingly trying to use HTTPS for it. 
  - Speculated Cause: A glance at stuff looked up for the issue suggested that it was due to a list of domains that the browser is aware of ahead of time to use HTTPS for from it having certain stuff in the past. (HSTS). This was not the cause because HSTS preload stuff does not apply to IP addresses. [\[1\]](https://support.mozilla.org/en-US/questions/1413426)
  - Identified Cause: An AI-assisted lookup of the issue revealed that firefox will try again with HTTPS if the HTTP one can't be connected to .**Simply put**: In firefox, trying to connect to an HTTP server before it is available, and then again when it is, will result in it silently trying HTTPS and continuing to use https on reloads. [\[1\]](https://ibb.co/BHRP2bGm) [\[2\]](https://ibb.co/Zp7FqRPt)
  - Identified Solution: Firefox will silently attempt to use HTTPS for the URL when the connection for HTTP doesn't go through, resulting in later refreshes still trying for HTTPS which won't be available. This can be fixed by setting ``browser.fixup.fallback-to-https`` to ``false`` in ``about:config``. [\[1\]](https://ibb.co/WpDtYJRs) [\[2\]](https://ibb.co/xtJPW4Cf)

## Discovery - 3 (services (nginx) is started and enabled automatically after installation on debian/ubuntu)
- Problem: All files were removed from ``/var/www/html/`` and Hello World was written to ``/var/www/html/index.html`` **after** installing nginx, and **before** starting and enabling it. When the server was connected to in the browser, the default nginx page was shown before the hello world one. 
- Identified Cause: Services added by packages on Ubuntu are started by default and also enabled [\[1\]](https://ibb.co/MygN4MM8) [\[2\]](https://serverfault.com/questions/861583/how-to-stop-nginx-from-being-automatically-started-on-install)
- Realistic solution: As debian & ubuntu automatically start and enable some of the installed packages and sometimes add firewall rules, we should use a distribution that is more predictable about this where possible (e.g., Rocky or Fedora).

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
  - It is preferable to have what is available on the returned object explicitly defined and be able to hover for information in an IDE. Example of an issue relating to AI generating code in exploring the problem: https://ibb.co/Kxj82zgf