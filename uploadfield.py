#!/usr/bin/python

import subprocess
import cgi
cgitb.enable()

$query = CGI::new();

# from https://docs.python.org/2/library/cgi.html
form = cgi.FieldStorage()

if "myfield.nc" not in form:
  subprocess.call("./htmlheader.cgi", shell=True, stderr=subprocess.STDOUT);
  subprocess.call("./myvinkhead.cgi error no_netcdf_file", shell=True, stderr=subprocess.STDOUT);
  subprocess.call("./myvinkfoot.cgi", shell=True, stderr=subprocess.STDOUT);
  raise SystemExit

kindname = form.getfirst('kindname','')
climfield = form.getfirst('climfield','')
EMAIL = form.getfirst('id','')

# copy dat (big binary) file to upload area
i = 0;
while os.path.exist("data/uploaded%i.nc" % i):
    i=i+1
  
outfile = open("data/uploaded%i.nc" % i)
ncfile = form["myfield.nc"]
if not ncfile.file:
  raise SystemExit
    
while 1:
    buffer = ncfile.file.read(1000000)
    if buffer == '':
        break
    outfile.write(buffer)
outfile.close()

# make a file with meta-metadata
$infofile = "$outfile";
if ($EMAIL =~ /^[\w_\-\.\+]+@[\w_\-\.]+$/) {
$infofile =~ s/\.[\w]*$/\.$EMAIL.info/;
open (OUTFILE,">$infofile");
print OUTFILE "$outfile\n";
if ($kindname =~ /^[\w\s_\-\/\+=\(\)]+$/) {
  print OUTFILE "$kindname\n";
} else {
  $result = system("./htmlheader.cgi");
  $result = system("./myvinkhead.cgi error invalid_kindname");
  $result = system("./myvinkfoot.cgi");
  exit(1);
}
if ($climfield =~ /^[\w\s_\-\/\+=\(\)]+$/) {
  print OUTFILE "$climfield\n";
} else {
  $result = system("./htmlheader.cgi");
  $result = system("./myvinkhead.cgi error invalid_climfield");
  $result = system("./myvinkfoot.cgi");
  exit(1);
}
close OUTFILE;
} else {
# Invalid email address.
$result = system("./htmlheader.cgi");
$result = system("./myvinkhead.cgi error invalid_email");
$result = system("./myvinkfoot.cgi");
exit(1);

# call select.cgi for the rest.
# set up the environment
$ENV{'EMAIL'} = $query->param('email');
$ENV{'FORM_field'} = $infofile;
$ENV{'kindname'}   = $kindname;
$ENV{'climfield'}  = $climfield;
$ENV{'file'}  = $outfile;

$result = system("./check_netcdf.cgi"); # already gives the error message
if ( $result == 0 ) {
  exec "./select.cgi";
}
