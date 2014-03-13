import sys
import os
import subprocess
import urllib
import logging
import logging.handlers


def getpngwidth(pngfile):

    cmd = "file {pngfile} | sed -e 's/^.*data, //' -e 's/ x .*$//'".format(pngfile=pngfile)
    width = subprocess.check_output(cmd, shell=True)

    width = float(width)
    halfwidth = width // 2

    if (2 * halfwidth) != width:
        halfwidth += 0.5

    return halfwidth


def launchScript(cmd):
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    print output


def initScript():
    launchScript('./init.cgi')


def headerScript(params, title=None):

    if not title:
        title = "KNMI Climate Change Atlas"
    os.environ['EMAIL'] = params.EMAIL
    args = ['./myvinkhead.cgi', title, '', '']
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = urllib.unquote(p.stdout.read())
    output = output.replace('451','600')
    output = output.replace('762','911')
    print output

def footerScript():
    launchScript('./climexp_footer.cgi')


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


def month2string(m):

    monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

    # TODO: emit an exception if not in dict
    cm = monthDict[m]
    return cm

def generateReport(params, error):
    """Generate a report and send it by email.

    Inputs:
    -------
      params: FormParameters object
      errro: Exception error
    """

    mailHost = 'smtp.prolocation.net'
    fromAddr = 'noreply@example.com'
    toAddrs = ['lemmel@stcorp.nl']
    subject = 'Automatic error message in climate explorer'
    credentials = None
    secure = None

    log = logging.getLogger('report')
    log.setLevel(logging.INFO)

    if 0:
        hdlr = logging.handlers.SMTPHandler(mailHost, fromAddr, toAddrs, subject,
                                            credentials, secure)
    else:
        hdlr = logging.StreamHandler(sys.stdout)
#        hdlr = logging.FileHandler('error_report.txt')

    hdlr.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(hdlr)

    message = ["Error message from Climate Explorer", '']
    message.extend(params.dump())

    errorMsg = ['']

    # TODO: check type of errorMsg
    errorMsg.append('Error: %s' % str(error))

    message.extend(errorMsg)

    log.debug('<br>\n'.join(message))

