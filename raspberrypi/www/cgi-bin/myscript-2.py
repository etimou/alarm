#!/usr/bin/python
import os

print "Content-Type: text/html"
print ""
print "<html>"
print "<h2>CGI Script Output</h2>"
print "<p>This page was generated by a Python CGI script.</p>"
print "</html>"

os.system('echo "CMD 11985906 1" > /dev/ttyAMA0')

