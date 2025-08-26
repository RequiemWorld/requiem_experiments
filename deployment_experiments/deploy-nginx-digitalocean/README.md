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

## Discovery 4 (yaml doesn't support tabs, cloud-init will not work with them)
- Problem: When experimenting and copying over the config and adjusting it multiple times resulted in it not working on the server.
- Identified Cause: I placed tabs in it for indentation, as it turns out YAML doesn't support tabs for indentation, only spaces. [\[1\]](https://stackoverflow.com/questions/19975954/a-yaml-file-cannot-contain-tabs-as-indentation)
- Chosen Solution: Introduce a helper class for putting together a cloud config imperatively, have the method for converting to a string handle the formatting, removing the risk of errors introduced by formatting manually. [\[1\]](https://ibb.co/k6XdsK2R) [\[2\]](https://ibb.co/Kjhmz8Hn)

## Discovery 5 (docker is picky about where arguments for things like run go)
- Problem: When practicing running a docker image in preparation for automation, the command did not work due to the ``--name``` argument being in the wrong place.
- Identified Cause: The named arguments for docker commands have to come after the first positional one, and before the final positional one, i.e. ``docker run --name <container_name>` and not `

## Discovery 6 (docker bypasses firewall rules on Debian & Ubuntu due to direct manipulation of iptables)
- Found in the documentation for installing on Ubuntu & Debian: https://docs.docker.com/engine/install/ubuntu/, https://docs.docker.com/engine/install/debian/
- Other distributions might have better firewall integration: It doesn't mention the same firewall compatibility issues for CentOS and Fedora. [\[1\]](https://ibb.co/VpPKGgxL) [\[2\]](https://ibb.co/Dg84HDHw) [\[3\]](https://ibb.co/nsgZK6Z4) 

## Discovery 7 (apt used/uses HTTP by default in some cases and requires separate packages for HTTPS support?)
- Suggested by AI when queried for the reason why digitalocean has this in articles for installing docker, it suggested that it is because older versions didn't technically need it for security of installing packages due to GPG signing. (take with a grain of salt, I'm not looking into this further. [\[1\]](https://ibb.co/nsD0pJnN)) [\[2\]](https://ibb.co/PvBmH0zj)

## Discovery 8 (apt install exits before files for nginx are created)
- Issue Encountered: The apt command presumably was exiting prior to the installation of nginx truly finishing. It was impossible to write various files to /usr/share/nginx/html/ without putting a sleep in place. Printing the command output revealed that the directory hadn't been created yet. [\[1\]](https://ibb.co/20p7n9mp)
- Possible Solution #1 (use docker): A docker image would presumably be more predictable to setup/configure, avoiding intermittency issues.
- Possible Solution #2 (poll directory until the file has been created): It might be necessary to check and wait for the file to be created.

## Discovery 9 (single quotes inside single quotes that are inside double quotes must be escaped)
- Issue Encountered: The command written to echo to a file was not working as intended due to a formatting issue. **Problematic command**: ``bash -c 'echo 'hello world333' > /usr/share/nginx/html/index.html'`` **Unintended Output**: ``hello\n`` [[\1\]](https://ibb.co/d4qjmCTG)
- Solution: Escape the quotation marks.

## Discovery 8 (impossible to overwrite /usr/share/nginx/index.html directly after installing with paramiko?)
- Issue Encountered: After installing nginx over ssh with paramiko, it was impossible to overwrite /usr/share/nginx/index.html. It was possible but challenging to write to any other file in the directory after installation as well.
- Speculated Issue: Files other than index.html were able to be written in the directory after with paramiko with some intermittency. The issue is probably due to the directory not being created and files placed when the apt command finishes. Adding a 10-second sleep fixed the issue/intermittency for non index.html files.
- Unresolved Issue: Overwriting index.html after installing nginx on Ubuntu with apt over ssh through Paramiko proved impossible. [\[1\]](https://ibb.co/XftcTxYn) [\[2\]](https://ibb.co/Jwj9wKxb)
- Possible Solution #1 (use docker): As installing packages from the repositories and configuring them is proving to be a burden, installing them through docker and configuring them there may be a better option.
- Possible Solution #2 (use another distro): Ubuntu and indirectly debian are proving themselves to be unreliable and burdensome for automation. Rocky Linux might be the better option.

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
- The usage of arguments for docker commands is annoying and should be less necessary to always remember
  - Example 1: To use important arguments such as ``name`` as part of the run command for making/starting a new container, it has to be ``docker run --name <name> <image>`` and not ``docker run <image> --name <name>``
  - The usage of various commands introduces the likelihood of human error in the positioning being missed or the arguments being used wrong. This is something that code can be used to tackle the complexity of with helper functions or classes.
  - We're going to be scripting stuff up to employ whole servers and finding out after that something was off in writing when it could have been prevented. A more efficient way to work with stuff could be provided in many situations.