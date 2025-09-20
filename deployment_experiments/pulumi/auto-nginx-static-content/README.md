## Discovery #1 - apt upgrade -y may block indefinitely as part of user_data
- Identified Problem: apt upgrade -y will block and potentially take down SSH when used as part of the user_data e.g. ``#!/bin/bash\napt update -y \napt upgrade -y\napt install nginx`` [\[1\]](https://ibb.co/XkCDXK7Y) [\[2\]](https://ibb.co/WWMcXs5p)
- Identified Solution: setting the environment variable ``DEBIAN_FRONTEND=noninteractive`` will prevent apt from prompting the user for anything and prevent it from locking up. 
