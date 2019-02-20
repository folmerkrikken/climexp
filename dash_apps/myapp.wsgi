#!/home/folmer/anaconda3/bin/python
import sys
sys.path.insert(0,'/var/www/climexp/dash_apps')
#from sop_app import server as app
from sop_app import server as app
print(sys.path)
#from test_app import app as application
application = app

