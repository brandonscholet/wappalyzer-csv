# wappybird

Multithreaded Wappalyzer CLI tool to find Web Technologies, with optional CSV output.

Allows multiple methods of input, including files, urls, and STDIN. Provided jsut the hostname, it will attempt to access via HTTPS and then HTTP, allowing redirects.

based originally on the wappalyzer-cli by gokulapap

Now uses the updated files from the npm-based [Wappalyzer](https://github.com/wappalyzer/wappalyzer/), instead of the static file from the [python-Wappalyzer](https://github.com/chorsley/python-Wappalyzer) library.

# Installation :

> pip uninstall python-Wappalyzer -y || sudo pip uninstall python-Wappalyzer -y

> git clone https://github.com/brandonscholet/python-Wappalyzer.git

> cd python-Wappalyzer/

> sudo python setup.py install

> cd ..

> git clone https://github.com/brandonscholet/wappybird

> cd wappybird

> sudo python setup.py install

# Hella Input Examples:

> wappy -u \<URL\> <URL>

> wappy -f <file> <file2> -u <URL>

> wappy -f <file> -u <URL> -f <file2> <file3> 

> subfinder -d example.com | wappy -wf <output.csv> -q -t 25

> echo <URL>,<URL>,<URL> | wappy -q

> echo <URL> <URL> <URL> | wappy 

# Usage

```
─$ wappy -h
usage: wappy [-h] [-u URL [URL ...]] [-f FILE [FILE ...]] [-wf WRITEFILE]
             [-t THREADS] [-q]

Note: This program also accepts hosts from STDIN with space, comma or newline delimiters.

Finds Web Technologies!

options:
  -h, --help            show this help message and exit
  -u URL [URL ...], --url URL [URL ...]
                        url to find technologies
  -f FILE [FILE ...], --file FILE [FILE ...]
                        list of urls to find web technologies
  -wf WRITEFILE, --writefile WRITEFILE
                        File to write csv output to
  -t THREADS, --threads THREADS
                        How many threads yo?
  -q, --quiet           Don't want to see any errors?

```

# Demo 
<img src="https://github.com/brandonscholet/wappybird/blob/master/walkthrough.gif?" width=750>
