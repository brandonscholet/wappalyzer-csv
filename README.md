# wappybird
Multithreaded Wappalyzer CLI tool to find Web Technologies 

based on the wappalyzer-cli by gokulapap

Now uses the updated files from Wappalyzer, isntead of the static file from the semi-unmaintained wappalyzer-cli

# Installation :

> pip uninstall python-Wappalyzer || sudo pip uninstall python-Wappalyzer

> git clone https://github.com/chorsley/python-Wappalyzer.git

> cd python-Wappalyzer/

> sudo python setup.py install

> cd ..

> git clone https://github.com/brandonscholet/wappybird

> cd wappybird

> sudo python setup.py install

```
─$ ./wappy  -h
usage: wappybird [-h] [-u URL] [-f FILE] [-wf WRITEFILE] [-t THREADS] [-q]

Finds Web Technologies!

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     url to find technologies
  -f FILE, --file FILE  list of urls to find web technologies
  -wf WRITEFILE, --writefile WRITEFILE
                        File to write csv output to
  -t THREADS, --threads THREADS
                        How many threads yo?
  -q, --quiet           Don't want to see any errors?

```

# Demo 
![wappy](https://user-images.githubusercontent.com/57899332/141133098-906e9ac0-b85e-453d-9e16-f48b4c14303c.gif)
