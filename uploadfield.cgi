#!/usr/bin/perl

use CGI

$query = CGI::new();

# from http://stein.cshl.org/WWW/software/CGI/cgi_docs.html
# we have version 2.36, so upload() is unavailable
$NCFILE  = $query->param('myfield.nc');
$kindname = $query->param('kindname');
$climfield = $query->param('climfield');
$EMAIL = $query->param('email');

if ( $NCFILE ) {
  # copy dat (big binary) file to upload area
  $i = 0;
  do {
    $outfile = "data/uploaded".$i++.".nc";
  } until not -e $outfile;
  
  open (OUTFILE,">$outfile");
  while ( $bytesread=read($NCFILE,$buffer,1024) ) {
    print OUTFILE $buffer;
  }
  close OUTFILE;
  # make a file with meta-metadata
  $infofile = "$outfile";
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
  $result = system("./htmlheader.cgi");
  $result = system("./myvinkhead.cgi error no_netcdf_file");
  $result = system("./myvinkfoot.cgi");
  exit(1);
}

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
