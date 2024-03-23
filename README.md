# Documentation

In Windows terminal run ``pip install python-decouple`` the package where ``config`` module is used to set up seperate settings while running our project

* Now go to the project directory using ``cd`` command

* Now run ``SET PORT=8000`` (We can give any other port but make sure to set the same address while setting up the proxy)

* Now open the system settings and search for proxy (on client side) and set the IP address as ``localhost`` and port 8000 or something that is set in terminal

* Now run ``python server.py`` in the terminal

* Now verify by logging to any webiste like ``http://www.vulnweb.com/`` can see the website (Any HTTP website will work)
  The reason for HTTPS not working is there is a requirement for SSL certificates
