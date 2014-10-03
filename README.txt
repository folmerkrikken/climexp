General informations about the website "Climate Explorer"
=========================================================

URL : http://climexp.knmi.nl/plot_atlas_form.py

The website is hosted on the server 'bhlclim'.
A copy of this server (without the data) is available at 'bvlclim'.
You can reach both of these servers via the login 'oldenbor'.


Info. about 'bhlclim'
---------------------

In the server 'bhlclim', the most significant folders/files are the following:
- /home/oldenbor/local/bin                      : Contains gnuplot 4.6.
- /home/oldenbor/bin/python                     : Python 2.7.
- /home/oldenbor/climexp/bin                    : Some executables from Geert Jan Oldenborgh.
- /home/oldenbor/CMIP5                          : The data to process.
- /home/oldenbor/atlas                          : The processed data.
- /home/oldenbor/template/plot_atlas_form.htm   : A HTML template.
- /home/oldenbor/plot_atlas_form.py             : The CGI python script used to display the HTML formular.
- /home/oldenbor/plot_atlas_map.py              : The file that contains the Python class to generate a map.
- /home/oldenbor/plot_atlas_series.py           : The file that contains the Python class to generate a time series.
- /home/oldenbor/formparamters.py               : Python class that contains the parameters coming from the HTML formular.
- /home/oldenbor/settings.py                    : Python class that contains the configuration for the website

Info. about 'plot_atlas_form.py'
--------------------------------

Some remarks for 'plot_atlas_form.py':
- JINJA2 (The Python template engine) is used to generated the html code.
- Don't forget to put the shebang #!/home/oldenbor/bin/python .
- If you want to enable the debugging mode, you can remove the comments 
  around 'import cgitb; cgitb.enable()'
- You can use the function 'util.generateReport(params, e)' to generate and
  to send more elaborated reports. This function doesn't work, you have 
  to modify it.


