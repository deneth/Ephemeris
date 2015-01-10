#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sqlite3
import re
from time import sleep, localtime, strftime
import commands
import sys

path = "./"

# Download meteofrance index.html and save it in path+tmp
# Delete previous file
commands.getstatusoutput('/bin/rm '+path+'tmp/index.html')
# wget http://france.meteofrance.com/
commands.getstatusoutput('cd '+path+'tmp/ && curl http://www.meteofrance.com/accueil > index.html')

Fete = "x"
SolLever = "x"
SolCoucher = "x"
LuneLever = "x"
LuneCoucher = "x"

today = strftime("%Y-%m-%d", localtime())
# Open file to read data
with open(path+'tmp/index.html', 'r') as f:
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

print("SolLever: %s" % SolLever)
print("SolCoucher: %s" % SolCoucher)
print("LuneLever: %s" % LuneLever)
print("LuneCoucher: %s" % LuneCoucher)
print("Fete: %s" % Fete)

# Save data in the DB
con = None
try:
    conn = sqlite3.connect(path+'public/database/PiHomeConnect.sqlite')
    sql_command = "INSERT INTO Ephemeride VALUES('"+today+"', '"+Fete+"', '"+SolLever+"', '"+SolCoucher+"', '"+LuneLever+"', '"+LuneCoucher+"');"
    print("%s" % (sql_command))
    conn.execute(sql_command)
    conn.commit()

except sqlite3.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if conn:
        conn.close()
