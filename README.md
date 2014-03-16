# MaristFTPMock

Roughly simulates how the FTP server on the zOS mainframe behaves for job submissions.

## Install recipe

_This has only been tested with Python 2.7. It seems that the packaging is screwed up for Python 3 :'(_  
1. You need pip, make sure you have pip. Read [PIP Install Docs](http://pip.readthedocs.org/en/latest/installing.html#using-package-managers) and I suggest using the package manager for your system.
2. Install this using pip ```pip install git+https://github.com/niumainframe/ZosFtpMock.git```
  * Caveat: If you end up with a version of pip >= 1.5 then you have to add this flag in ```--process-dependency-links```
3. run by invoking ```zosftpd.py```
  * You can see command line options with the ```-h``` flag.  Some of which may not be implemented yet.
