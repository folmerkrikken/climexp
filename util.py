import subprocess
import urllib
import logging


def launchScript(*args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = urllib.unquote(p.stdout.read())
    print output

def initScript():
    launchScript('./init.cgi')

def headerScript(title=None):

    if not title:
        title = "KNMI Atlas <font color=\"#ff2222\">WORK IN PROGRESS</font>"
    launchScript('./myvinkhead.cgi', title, 'Choose parameters', '')

def footerScript():
    launchScript('./myvinkfoot.cgi')

class JavascriptFormatter(logging.Formatter):
    fmt = '%(asctime)s %(name)s: %(message)s'
   
    def format(self, record):

        if record.levelno == logging.DEBUG:
            self._fmt = "<script language=\"javascript\">console.debug(\"%(asctime)s DEBUG - %(name)s: %(message)s\")</script>"
        elif record.levelno == logging.INFO: 
            self._fmt = "<script language=\"javascript\">console.info(\"%(asctime)s %(name)s: %(message)s\")</script>"
        elif record.levelno == logging.ERROR: 
            self._fmt = "<script language=\"javascript\">console.error(\"%(asctime)s %(name)s: %(message)s\")</script>"
        elif record.levelno == logging.WARNING: 
            self._fmt = "<script language=\"javascript\">console.warn(\"%(asctime)s %(name)s: %(message)s\")</script>"
        else:
            self._fmt = "<script language=\"javascript\">console.log(\"%(asctime)s %(name)s: %(message)s\")</script>"

        result = logging.Formatter.format(self, record)
        return result

