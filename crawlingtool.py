import urllib3
import os
import shutil
import zipfile
import sc2reader
import time

###################################################################################
# A script to download zip files of all the replays from a spawningtool.com query #
###################################################################################

# The query is included in the URL parameters, tag=13 is ZvZ matches only
url = 'https://lotv.spawningtool.com/zip/?before_time=&coop=&after_played_on=&query=&after_time=&patch=&tag=13&pro_only=on&order_by=&before_played_on=&p='
# Range of pages to download.
firstPage = 1
lastPage = 100
# Amount of pages to download before we take a break to not get blocked
iteration = 6;


path = os.getcwd();
urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE')
x = firstPage
while x < lastPage:
	for y in range(1, iteration):
		print("Downloading page {0}...".format(x))
		pathx = path + "/page" + str(x) + ".zip"
		urlx = url + str(x)

		with open(pathx, 'wb') as out:
			r = http.request('GET', urlx, preload_content=False)
			shutil.copyfileobj(r, out)

		r.release_conn()
		x += 1

	print("sleeping....")
	time.sleep(60)
