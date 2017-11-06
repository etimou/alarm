#!/usr/bin/python
print "Content-Type: text/html"
print ""
print "<html>"
print "<h2>Etat des capteurs</h2>"

print '<table border="1">'
print "<tr>"
print "<td>Capteur</td>"
print "<td>Jour</td>"
print "<td>heure</td>"
print "</tr>"

for line in open('/home/pi/record'):
  lineSpl = line.split(' ')
  print "<tr>"
  print "<td>"+lineSpl[0]+"</td>"
  print "<td>"+lineSpl[1]+"</td>"
  print "<td>"+lineSpl[2]+"</td>"
  print "</tr>"

print "</table>" 


print '<a href="../index.html">Retour page principale</a>' 
print "</html>"
