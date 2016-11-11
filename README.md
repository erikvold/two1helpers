# two1helpers

This repo contains modules with helper functions for writing Python programs for the 21 platform.

## two1data

This module contains functions that are helpful in passing information via the *21 buy* command with the _--data_ and _--data-file_ flags. Using the functions currently requires four files: two1data.py, __init__.py, config.ini, and two1test-server.py.

### jshon2shell

config.ini must be customized so that the variable _pathtobin_ is defined as, yes, /path/to/bin, e.g. /usr/games/fortune.

The server must be launched via *python3 two1test-server.py*.  The -d flag is optional.

The test shell command *test/riddles* will issue:

*21 buy "http://[::]:9999/test" --data '{"options" : "riddles"}'*

This will pass "riddles" to two1test-server.py, which will look in config.ini for the value of _pathtobin_, then issue *fortune riddles*.  (The riddles database is available on most Linux systems by default; if this produces an error, try passing "literature".)

This method of passing options is very flexible but there is a security issue which is addressed by using shlex.quotes() to escape the options string.



