#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sqlite3
import re
from time import sleep, localtime, strftime
import commands
import MySQLdb as mdb

path = "/home/pi/www/tmp/"

# Download meteofrance index.html and save it in /var/www/tmp
# Delete previous file
commands.getstatusoutput('/bin/rm '+path+'index.html')
# wget http://france.meteofrance.com/
commands.getstatusoutput('cd '+path+' && wget http://www.meteofrance.com/accueil')

Fete = "x"
SolLever = "x"
SolCoucher = "x"
LuneLever = "x"
LuneCoucher = "x"

today = strftime("%Y-%m-%d", localtime())
# Open file to read data
with open(path+'index.html', 'r') as f:
	page_source = f.read()

	m = re.search('<div class="mod-ephemeride-line mod-ephemeride-line-first">.+<img src="/mf3-base-theme/images/contents/ephemeride-jour.png" alt="Soleil" />.+<span>Lever&nbsp;: <strong>(.+?)</strong></span>.+<span>Coucher&nbsp;: <strong>(.+?)</strong></span>.+</div>.+<div class="mod-ephemeride-line">',page_source,re.DOTALL) 
	if m:
		SolLever = m.group(1)
		SolCoucher = m.group(2)
	m = re.search('<div class="mod-ephemeride-line">.+<img src="/mf3-base-theme/images/contents/ephemeride-nuit.png" alt="Lune" />.+<span>Lever&nbsp;: <strong>(.+?)</strong></span>.+<span>Coucher&nbsp;: <strong>(.+?)</strong></span>',page_source,re.MULTILINE|re.DOTALL) 
	if m:
		LuneLever = m.group(1)
		LuneCoucher = m.group(2)
	m = re.search('<div class="mod-ephemeride">.*<h2 class="capitalize">.*</h2>.*<span class="mod-ephemeride-saint">(.+?)</span><br>', page_source,re.MULTILINE|re.DOTALL)
	if m:
		Fete = m.group(1)

f.close()

print Fete
print SolLever
print SolCoucher
print LuneLever
print LuneCoucher

con = mdb.connect('localhost', 'root', 'raspberry', 'MonitoringPi');
cur = con.cursor()
with con:
		query = "DELETE FROM Ephemerides WHERE date(date)=date(now())";
		cur.execute(query);
		
		query = ( "INSERT INTO Ephemerides ( fete, sollever, solcoucher, lunelever, lunecoucher) "
						"VALUES (%(fete)s, %(sollever)s, %(solcoucher)s, %(lunelever)s, %(lunecoucher)s)")
		data = {
			'fete': Fete,
			'sollever': SolLever,
			'solcoucher': SolCoucher,
			'lunelever': LuneLever,
			'lunecoucher': LuneCoucher,
		}
		
		cur.execute(query, data)