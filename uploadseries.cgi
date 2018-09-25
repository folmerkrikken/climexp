#!/usr/bin/perl

use CGI;

$query = CGI::new();

# from http://stein.cshl.org/WWW/software/CGI/cgi_docs.html
# we have version 2.36, so upload() is unavailable
$NCFILE  = $query->param('myfield.nc');

# copy dat (binary) file to upload area
$i = 0;
do {
  $outfile = "data/uploaded".$i++;
} until not -e $outfile.".nc";

open (OUTFILE,">$outfile".".nc");
while ( $bytesread=read($NCFILE,$buffer,1024) ) {
    print OUTFILE $buffer;
}
close OUTFILE;

open (LOGFILE,">/tmp/uploadseries.log");
$type = $query->param('type');
$type =~ s/[^A-Za-z0-9 ]*//g;
print LOGFILE "outfile = $outfile\n";
print LOGFILE "type = $type\n";
if ( $type =~ /p/ ) {
  $type='p';
  $NAME = 'precipitation';
} elsif ( $type =~ /t/ ) {
  $type='t';
  $NAME = 'temperature';
} elsif ( $type =~ /s/ ) {
  $type='s';
  $NAME = 'pressure';
} elsif ( $type =~ /l/ ) {
  $type='s';
  $NAME = 'sea level';
} else {
  $type = 'i';
  $NAME = 'index';
}
print LOGFILE "NAME = $NAME\n";
chomp($cwd = `pwd`);
print LOGFILE "cwd = $cwd\n";
$email = $query->param('email');
$email =~ s/[^A-Za-z0-9 @.]*//g;
print LOGFILE "email = $email\n";
$station = $query->param('station');
$station =~ s/[^A-Za-z0-9 _-]*//g;
if ( $station =~ /^$/ ) {
    $station = $email;
}
print LOGFILE "station = $station\n";
close LOGFILE;

# call getdata.cgi for the rest.
# set up the environment
$ENV{'STATION'} = $station;
$ENV{'EMAIL'}   = $email;
$ENV{'DIR'}     = $cwd;
$ENV{'TYPE'}    = $type;
$ENV{'NAME'}    = $NAME;
$ENV{'WMO'}     = $outfile;
$ENV{'PROG'}    = "netcdf2dat $outfile".".nc";
$ENV{'file'}    = $outfile.".nc";

$result = system("./check_netcdf.cgi");
if ( $result == 0 ) {
  exec "./getdata.cgi";
}
